import logging
import os
import shutil
import signal
import time
from typing import Any, Union

import pandas as pd
import copy
import numpy as np
from cdsetool.credentials import Credentials
from cdsetool.download import download_features
from cdsetool.monitor import Status, StatusMonitor
from cdsetool.query import query_features

from util.input_sentinel_class import InputSentinelClass

# MINUTES_BEFORE_SIGNAL = 10
# LOGGER_NAME = "Download_logger"
# LOGGER = logging.getLogger(LOGGER_NAME)
# CDSELOGGER = logging.getLogger("CDSE_logger")


# if not LOGGER.handlers:
#     _h = logging.StreamHandler()
#     _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
#     LOGGER.addHandler(_h)
# LOGGER.setLevel(logging.INFO)

# if not CDSELOGGER.handlers:
#     _h_cdse = logging.StreamHandler()
#     _h_cdse.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
#     CDSELOGGER.addHandler(_h_cdse)
# CDSELOGGER.setLevel(logging.INFO)


def _format_query_bounds(start_date: str, end_date: str) -> tuple[str, str]:
    """Normalize date bounds to CDSE millisecond-precision timestamps."""
    qdate1 = start_date
    qdate2 = end_date

    if "T" not in qdate1:
        qdate1 = f"{qdate1}T00:00:00.000Z"
    else:
        qdate1 = qdate1.replace("T00:00:00Z", "T00:00:00.000Z")
        qdate1 = qdate1.replace("T00:00:00.00Z", "T00:00:00.000Z")

    if "T" not in qdate2:
        qdate2 = f"{qdate2}T23:59:59.999Z"
    else:
        qdate2 = qdate2.replace("T00:00:00Z", "T23:59:59.999Z")
        qdate2 = qdate2.replace("T00:00:00.00Z", "T23:59:59.999Z")

    return qdate1, qdate2


def get_just_df_from_query(
    sentinel_1: bool,
    df,
    date1: str,
    date2: str,
    credentials: Any = None,
    proxy: Any = None,
):
    if sentinel_1:
        df_, _ = get_query_sentinel_1(df, date1, date2, credentials, proxy=proxy)
        return df_

    df_ = get_query_sentinel_2(df, date1, date2, credentials, proxy=proxy)
    return df_


def download_products_for_dates(
    sentinel_1: bool,
    df,
    date1: str,
    date2: str,
    credentials: Any = None,
    directory: str = None,
    geojson_name: Any = None,
    proxy: Any = None,
) -> Any:
    del geojson_name

    if sentinel_1:
        print("Inside wrapper (download_products_for_dates), query for sentinel 1 started")
        df_, _ = get_query_sentinel_1(df, date1, date2, credentials, proxy=proxy)
        print("Inside wrapper (download_products_for_dates), query for sentinel 1 ended")
        download_product_cdse(
            df=df_,
            products_dir=directory,
            username=credentials.name,
            password=credentials.password,
            tmp_path_same_folder_dwl=True,
            proxy=proxy,
        )
        return True, df_

    print("Inside wrapper (download_products_for_dates), query for sentinel 2 started")
    df_ = get_query_sentinel_2(df, date1, date2, credentials, proxy=proxy)
    print("Inside wrapper (download_products_for_dates), query for sentinel 2 ended")
    download_product_cdse(
        df=df_,
        products_dir=directory,
        username=credentials.name,
        password=credentials.password,
        tmp_path_same_folder_dwl=True,
        proxy=proxy,
    )
    return True, df_


def get_query_sentinel_1(
    df,
    startDate: str,
    endDate: str,
    credentials: Any = None,
    proxy: Any = None,
):
    del credentials
    del proxy

    qdate1, qdate2 = _format_query_bounds(startDate, endDate)
    features_list = []

    for _, item in df.iterrows():
        collection = "SENTINEL-1"
        search_terms = {
            "contentDateStartGe": qdate1,
            "contentDateStartLe": qdate2,
            "productType": "SLC",
            "operationalMode": "IW",
            "relativeOrbitNumberEq": int(item["Rel. orbit number"]),
            "geometry": item["esaquerypoint"],
            "processingLevel": "LEVEL1",
            "timeliness": "NRT-3h",
        }

        try:
            features = query_features(collection, search_terms, options={"expand_attributes": True})
        except Exception as e:
            print("Error querying Sentinel-1 features: %s" % e)
            continue

        for f in features:
            if not f["Online"]:
                continue

            attributes = {x["Name"]: x["Value"] for x in f["Attributes"]}
            f["title"] = f["Name"]
            attributes["title"] = f["Name"]
            f["relativeOrbitNumber"] = attributes["relativeOrbitNumber"]
            f["startDateStr"] = f["ContentDate"]["Start"][:10]
            f["updatedStr"] = f["ModificationDate"]
            f["sector"] = item["Name"]
            f["Name"] = item["Name"]
            f["burstGeometry"] = list(item["geometry"].exterior.coords)
            if "Burst ID" not in f and "Burst ID" in item:
                f["BurstID"] = item["Burst ID"]
            f["properties"] = attributes
            f["orbitDirection"] = f["properties"].get("orbitDirection")

            if "geometry" not in f:
                f["geometry"] = f["GeoFootprint"]
            f["id"] = f["Id"]
            features_list.append(f)

    out_df = pd.DataFrame.from_dict(features_list)
    if out_df.empty:
        print("No Sentinel-1 products found for the given query")
        return out_df, features_list

    out_df = out_df.sort_values("startDateStr", ascending=True)
    out_df = out_df.sort_values("updatedStr", ascending=False).drop_duplicates(["sector", "startDateStr"])
    out_df = out_df.sort_index(inplace=False).reset_index(drop=True)
    return out_df, features_list


def download_product_cdse(
    df,
    products_dir,
    username: str,
    password: str,
    tmp_path_same_folder_dwl: bool,
    proxy=None,
):
    del proxy

    if df.empty:
        print("No products to download")
        return

    df = df.drop_duplicates(subset="id", inplace=False)
    features_list = df.to_dict(orient="records")
    credentials = Credentials(username, password)

    options = {"credentials": credentials, "concurrency": 4, "monitor": FileStatusMonitor()}
    if tmp_path_same_folder_dwl:
        options["tmpdir"] = products_dir

    print("Starting download of %s products into %s" % (len(features_list), products_dir))
    res = download_features(features_list, products_dir, options)
    for feature_id in res:
        print("feature %s downloaded" % feature_id)

    print("Download ended")


def get_query_sentinel_2(
    df,
    date1: str,
    date2: str,
    credentials: Any = None,
    proxy: Any = None,
):
    del credentials
    del proxy

    qdate1, qdate2 = _format_query_bounds(date1, date2)
    features_list = []

    for _, item in df.iterrows():
        collection = "SENTINEL-2"
        search_terms = {
            "contentDateStartGe": qdate1,
            "contentDateStartLe": qdate2,
            "productType": "S2MSI2A",
            "tileId": item["Name"],
            "geometry": item["esaquerypoint"],
        }

        try:
            features = query_features(collection, search_terms, options={"expand_attributes": True})
        except Exception as e:
            print("Error querying Sentinel-2 features for tile %s: %s" % (item["Name"], e))
            continue

        for f in features:
            if not f["Online"]:
                continue

            attributes = {x["Name"]: x["Value"] for x in f["Attributes"]}
            f["title"] = f["Name"]
            attributes["title"] = f["Name"]
            f["tileId"] = attributes["tileId"]
            f["relativeOrbitNumber"] = attributes["relativeOrbitNumber"]
            f["startDateStr"] = f["ContentDate"]["Start"][:10]
            f["updatedStr"] = f["ModificationDate"]
            f["sector"] = "T{}_R{:03d}".format(f["tileId"], f["relativeOrbitNumber"])
            f["Name"] = f["sector"]
            if "geometry" not in f:
                f["geometry"] = f["GeoFootprint"]
            f["properties"] = attributes
            f["id"] = f["Id"]
            features_list.append(f)

    out_df = pd.DataFrame.from_dict(features_list)
    if out_df.empty:
        print("No Sentinel-2 products found for the given query")
        return out_df

    out_df = out_df.sort_values("startDateStr", ascending=True)
    out_df = out_df.sort_values("updatedStr", ascending=False).drop_duplicates(["sector", "startDateStr"])
    out_df = out_df.sort_index(inplace=False).reset_index(drop=True)
    return out_df


def connect_prod_lists_max(self, df_new, df_pre):
    """
    Insert the last product from df_pre as first item into the products list of df_new.
    """
    del self

    assert np.all(df_new.Name == df_pre.Name)
    df = pd.DataFrame(copy.deepcopy(df_new.to_dict()))

    df["lastprod"] = df_pre["products"].map(lambda odict: {next(reversed(odict)): odict[next(reversed(odict))]})
    df["lastkey"] = df_pre["products"].map(lambda odict: next(reversed(odict)))

    for _, row in df.iterrows():
        row.products.update(row.lastprod)
        row.products.move_to_end(row.lastkey, last=False)

    df = df.drop(columns=["lastprod", "lastkey"])
    return df


def connect_prod_lists(self, df_new, df_pre):
    """
    Insert the last product from df_pre as first item into the products list of df_new.
    """
    del self

    assert np.all(df_new.Name == df_pre.Name)
    df = pd.DataFrame(copy.deepcopy(df_new.to_dict()))

    the_new_dict_products = {}
    for key in df_pre["products"].keys():
        if df_pre["products"][key]["last_product"]:
            first_element = df_pre["products"][key]
            first_element["index"] = 0
            the_new_dict_products[key] = first_element

    for key in df["products"].keys():
        iter_element = df["products"][key]
        iter_element["index"] = iter_element["index"] + 1
        the_new_dict_products[key] = iter_element

    df["products"] = the_new_dict_products
    return df


def proxy_set(proxy: Any):
    proxy_ = {}
    if proxy.https_host != "" and proxy.https_port:
        proxy_["https"] = f"{proxy.https_host}:{proxy.https_port}"
    if proxy.http_host != "" and proxy.http_port is not None:
        proxy_["http"] = f"{proxy.http_host}:{proxy.http_port}"
    return proxy_


def bytes_to_human(num_bytes: int) -> str:
    if num_bytes < 1000:
        return f"{num_bytes} B"
    if num_bytes < 1000000:
        return f"{num_bytes / 1000:.2f} KB"
    if num_bytes < 1000000000:
        return f"{num_bytes / 1000000:.2f} MB"
    if num_bytes < 1000000000000:
        return f"{num_bytes / 1000000000:.2f} GB"

    return f"{num_bytes / 1000000000000:.2f} TB"


class FileStatusMonitor(StatusMonitor):
    line_length: int = 80

    __is_running: bool = True
    __done = []
    __status = []

    def run(self) -> None:
        while True:
            if self.__is_running is False:
                break
            if len(self.__status) > 0:
                for status in self.__done:
                    print(status.done_line())
            self.__draw()
            time.sleep(30)

    def start(self) -> None:
        def _set_line_length(_signal_num: Union[int, None], _stack) -> None:
            self.line_length, _ = shutil.get_terminal_size()

        _set_line_length(None, None)

        try:
            if os.name != "nt":
                signal.signal(signal.SIGWINCH, _set_line_length)
            super().start()
        except Exception as e:
            print("Error starting monitor: %s" % e)

    def stop(self) -> None:
        self.__is_running = False

    def status(self) -> "Status":
        status = Status(self)
        self.__status.append(status)
        return status

    def remove_status(self, status: "Status") -> None:
        self.__done.append(status)
        self.__status.remove(status)

    @property
    def __total_downloaded(self) -> int:
        return sum(status.downloaded for status in self.__status) + sum(status.size for status in self.__done)

    def __draw(self) -> None:
        print(
            " | ".join(
                [
                    "[[ ",
                    f"{len(self.__status)} files in progress",
                    f"{len(self.__done)} files done",
                    f"{bytes_to_human(self.__total_downloaded)} total downloaded",
                ]
            )
        )


# Backward-compatible wrappers used in this project.
def get_query_sentinel1(df, downl_params: InputSentinelClass):
    return get_query_sentinel_1(df, downl_params.startDate, downl_params.endDate)


def get_query_sentinel2(df, downl_params: InputSentinelClass):
    return get_query_sentinel_2(df, downl_params.startDate, downl_params.endDate)


def download_products(df, products_dir, username: str, password: str, tmp_path_same_folder_dwl: bool):
    return download_product_cdse(df, products_dir, username, password, tmp_path_same_folder_dwl)


def download_products_new(features, products_dir, username=str, password=str):
    credentials = Credentials(username, password)
    options = {"credentials": credentials, "concurrency": 4, "monitor": FileStatusMonitor()}
    print("Starting download of %s products into %s" % (len(features), products_dir))
    list(download_features(features, products_dir, options))

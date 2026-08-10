import csv
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


U = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"
OUT_FILE = "2023.csv"
FIELDS = ["ISIN","Bond Code","Issuer","Bond Type","Issue Date","Latest Rating"]




def get_page(page_no):
    data = {
        "pageNo":page_no,
        "pageSize":15,
        "isin":"",
        "bondCode":"",
        "issueEnty":"",
        "bondType":"100001",
        "couponType":"",
        "issueYear":"2023",
        "bondSpclPrjctVrty":"",
    }
    req = Request(
        U,
        data=urlencode(data).encode(),
        headers={"User-Agent":"Mozilla/5.0"},
    )
    with urlopen(req, timeout=20) as response:
        return json.load(response)["data"]


def main():
    first = get_page(1)
    bonds = first["resultList"]

    for page_no in range(2, first["pageTotal"] + 1):
        bonds.extend(get_page(page_no)["resultList"])

    with open(OUT_FILE,"w",newline="",encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file,fieldnames=FIELDS)
        writer.writeheader()
        for bond in bonds:
            writer.writerow({
                "ISIN": bond.get("isin",""),
                "Bond Code": bond.get("bondCode",""),
                "Issuer": bond.get("entyFullName",""),
                "Bond Type": bond.get("bondType",""),
                "Issue Date": bond.get("issueStartDate",""),
                "Latest Rating": bond.get("debtRtng",""),
            })

    print("saved",len(bonds),"rows to",OUT_FILE)


if __name__ == "__main__":
    main()

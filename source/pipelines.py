import pandas as pd


class StoreInfoPipeline(object):
    def process_item(self, item, spider):
        return item


class XlsxWriterPipeline:

    def __init__(self):
        self.dataframes = {}
        self.output_filename = None
        self.writer = None

    def open_spider(self, spider):
        self.output_filename = "results/%s.xlsx" % spider.name
        self.writer = pd.ExcelWriter(self.output_filename, engine="xlsxwriter")

    def close_spider(self, spider):
        sheet_number = 1
        for df_key in self.dataframes.keys():
            df = self.dataframes[df_key]
            sheet_name = 'Sheet %d' % sheet_number
            df.drop_duplicates(inplace=True)
            if spider.name == "maac" and "url_2" in df:
                if df[df.url_2.notna()].isnull:
                    df = df.drop("url_2", 1)
                df.to_excel(self.writer, index=False, sheet_name='MAAC Clubs', freeze_panes=(1, 0))
            else:
                df.to_excel(self.writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
            sheet_number += 1
        self.writer.save()

    def process_item(self, item, spider):
        if type(item) != dict:
            item_dict = vars(item)['_values']
        else:
            item_dict = item

        df_key = "".join(item_dict.keys())
        if df_key in self.dataframes.keys():
            self.dataframes[df_key] = self.dataframes[df_key].append(item_dict, ignore_index=True)
        else:
            self.dataframes[df_key] = pd.DataFrame([item_dict], columns=item_dict.keys())

        return item
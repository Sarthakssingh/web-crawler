BOT_NAME = 'source'

SPIDER_MODULES = ['source.utils']
NEWSPIDER_MODULE = 'source.utils'

ROBOTSTXT_OBEY = False


ITEM_PIPELINES = {
    'source.pipelines.XlsxWriterPipeline': 300,
}


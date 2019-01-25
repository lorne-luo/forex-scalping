from pyspark import SparkContext, SQLContext
from pyspark.sql.types import StructType, StructField, DecimalType, StringType, DateType

sc = SparkContext()
sqlContext = SQLContext(sc)


def get_dataframe(filename='data/GBPUSD-2018-12-tick.csv'):
    # open high low close
    schema = StructType([
        StructField("symbol", StringType(), True),
        StructField("time", StringType(), True),
        StructField("bid", DecimalType(precision=10, scale=5), True),
        StructField("ask", DecimalType(precision=10, scale=5), True)]
    )
    # df = spark.read.csv('GBPUSD-2016-11-tick.csv', header='False', schema=schema)
    df = sqlContext.read.csv(filename, header='False', schema=schema)
    return df

df=get_dataframe()
count=df.count()

print(count)

def getrows(df, rownums=0):
    return df.rdd.take(rownums+1)[-1]

def f(x):
    return print(x.bid)

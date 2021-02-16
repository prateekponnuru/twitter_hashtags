import twint
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
from pyspark.sql.types import StringType

# Configure
c = twint.Config()
# c.Username = "realDonaldTrump"
c.Search = "data science"
# c.format = "Username: {username} | Tweet : {tweet}"
c.Hide_output = True
# c.show_hashtags = True
c.Pandas = True
# c.Store_pandas = True
c.Limit = 1

# Run
tweets = twint.run.Search(c)
columns = twint.storage.panda.Tweets_df.columns

df = twint.storage.panda.Tweets_df[['hashtags', 'tweet']]
sc = SparkContext.getOrCreate()
sc.setLogLevel('WARN')
spark = SparkSession(sc)
htags = sc.parallelize(df['hashtags'])
htags = htags.reduce(lambda x, y: x + y)

htags = spark.createDataFrame(htags, StringType())
# htags = sc.parallelize(df)
popular_tags = htags.withColumnRenamed('value', '#hashtag').groupBy('#hashtag')\
                            .agg(count('#hashtag').alias('freq')).orderBy(col('freq').desc())
popular_tags.limit(10).show(truncate=False)
sc.stop()
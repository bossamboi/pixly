from script import s3;

"""Upload bg.png file as bg4.png to AWS S3 bucket"""
s3.upload_file("./bg.png", "pixlyrithm25", "bg4.png");

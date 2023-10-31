import os
import requests
# from airflow import DAG
from airflow.decorators import dag, task
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import datetime


urls = {
    "user_purchase": "https://drive.google.com/file/d/1p8Q_QoCqdxnkKcpPLp15FDTFjSdTE_zk/view?usp=drive_web&authuser=0",
    "log_reviews": "https://drive.google.com/file/d/1MfTRyyiMMGLuZ-hOysmjiATCUEHkQoE6/view?usp=drive_web&authuser=0",
    "movie_reviews": "https://drive.google.com/file/d/1q-9kHMPHzyJhx-GpP93BqaLbW-pFRfGX/view?usp=drive_web&authuser=0"
}


# Define your DAG
@dag(
    dag_id='upload_csv_to_db_and_gcs',
    schedule_interval=None,  # Set your desired schedule interval
    start_date=days_ago(1),  # Adjust the start date as needed
    catchup=False,  # Set to False if you don't want historical runs
)
# Task to download user_purchase.csv and upload it to PostgreSQL
def ProcessFiles():
    # environment setup process is to create a PostgreSQL DB with one table
    create_user_purchase_table = PostgresOperator(
        task_id="create_user_purchase_table",
        postgres_conn_id="capstone_postgres",
        sql="""
            DROP TABLE IF EXISTS capstone.user_purchase;
            CREATE TABLE capstone.user_purchase (
                invoice_number varchar(10),
                stock_code varchar(20),
                detail varchar(1000),
                quantity int,
                invoice_date timestamp,
                unit_price numeric(8,3),
                customer_id int,
                country varchar(20)
            );""",
    )


    @task
    def get_user_purchase_data():
        # NOTE: configure this as appropriate for your airflow environment
        data_path = "/usr/local/airflow/dags/files/user_purchase.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        response = requests.request("GET", urls["user_purchase_url"])

        with open(data_path, "w") as local_user_purchase_file:
            local_user_purchase_file.write(response.text)

        postgres_hook = PostgresHook(postgres_conn_id="capstone_postgres")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        with open(data_path, "r") as local_user_purchase_file:
            cur.copy_expert(
                "COPY user_purchase FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                local_user_purchase_file,
            )
        conn.commit()  

    @task
    def get_data():
        # NOTE: configure this as appropriate for your airflow environment
        data_path = "/usr/local/airflow/dags/files/"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        for index, url in urls:  
            response = requests.request("GET", url)

            with open(data_path, "w") as file:
                file.write(response.text)




    # Task to upload movie_review.csv to Google Cloud Storage
    upload_movie_reviews_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src="/path/to/movie_review.csv",  
        dst="your-gcs-bucket-name/path/to/movie_review.csv",  # Replace with GCS bucket and path
        bucket_name="your-gcs-bucket-name",
        google_cloud_storage_conn_id="google_cloud_default",  # Your GCP connection ID
        dag=dag,
    )

    # Similarly, create another task to upload log_reviews.csv to GCS
    upload_log_reviews_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_log_reviews_to_gcs",
        src="/path/to/log_reviews.csv",  # Replace with the actual source file path
        dst="your-gcs-bucket-name/path/to/log_reviews.csv",  # Replace with GCS bucket and path
        bucket_name="your-gcs-bucket-name",
        google_cloud_storage_conn_id="google_cloud_default",  # Your GCP connection ID
        dag=dag,
    )

    # Set task dependencies
    [get_user_purchase_data(), upload_movie_reviews_to_gcs, upload_log_reviews_to_gcs]

dag = ProcessFiles()
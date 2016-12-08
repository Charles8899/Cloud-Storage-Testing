from operation import *

upload_oss(1000, 2 * 1024 * 1024, 'upload-result-oss-2m')
upload_cos(1000, 2 * 1024 * 1024, 'upload-result-cos-2m')
download_oss(1000, 2 * 1024 * 1024, 'download-result-oss-2m')
download_cos(1000, 2 * 1024 * 1024, 'download-result-cos-2m')
delete_oss(1000, 2 * 1024 * 1024, 'delete-result-oss-2m')
delete_cos(1000, 2 * 1024 * 1024, 'delete-result-cos-2m')



from operation import *

upload_oss(100, 50 * 1024 * 1024, 'upload-result-oss-50m')
upload_cos(100, 50 * 1024 * 1024, 'upload-result-cos-50m')
download_oss(100, 50 * 1024 * 1024, 'download-result-oss-50m')
download_cos(100, 50 * 1024 * 1024, 'download-result-cos-50m')
delete_oss(100, 50 * 1024 * 1024, 'delete-result-oss-50m')
delete_cos(100, 50 * 1024 * 1024, 'delete-result-cos-50m')



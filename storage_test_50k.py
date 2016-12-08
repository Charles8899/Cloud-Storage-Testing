from operation import *

upload_oss(10000, 50 * 1024, 'upload-result-oss-50k')
upload_cos(10000, 50 * 1024, 'upload-result-cos-50k')
download_oss(10000, 50 * 1024, 'download-result-oss-50k')
download_cos(10000, 50 * 1024, 'download-result-cos-50k')
delete_oss(10000, 50 * 1024, 'delete-result-oss-50k')
delete_cos(10000, 50 * 1024, 'delete-result-cos-50k')



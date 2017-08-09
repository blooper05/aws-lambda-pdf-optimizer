import boto3
import os
import subprocess

def lambda_handler(event, context):
    bucket   = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    tmp_path = '/tmp/' + filename.split('/')[-1]
    client   = boto3.client('s3')
    client.download_file(bucket, filename, tmp_path)

    out_file = filename.replace('originals', os.environ['OUT_BUCKET'])
    out_path = tmp_path + '-optimized'

    cmd  = 'gs '
    cmd += '-sDEVICE=pdfwrite '
    cmd += '-dCompatibilityLevel=1.4 '
    cmd += '-dPDFSETTINGS=/default '
    cmd += '-dAutoRotatePages=/None '
    cmd += '-dNOPAUSE '
    cmd += '-dQUIET '
    cmd += '-dBATCH '
    cmd += '-sOutputFile='
    cmd += out_path
    cmd += ' '
    cmd += tmp_path
    subprocess.check_call(cmd.strip().split(' '))

    client.upload_file(out_path, bucket, out_file)

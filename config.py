db_host = '127.0.0.1'
db_port = 8088
db_user = 'username'
db_pass = 'password'

measurements_databases = [
    {'name': 'scratch', 'entry': '"lustremon_scratch2"."autogen"'},
    {'name': 'ssd', 'entry': '"lustremon_highiops"."autogen"'}]

measurements = [
    {
        'name': 'Samples',
        'unit': 'samples',
        'measurements': [{'name': 'read', 'value': 'lustre.read_bytes.samples'},
                         {'name': 'write', 'value': 'lustre.write_bytes.samples'}]
    },
    {
        'name': 'Sum',
        'unit': 'size [B]',
        'measurements': [{'name': 'read', 'value': 'lustre.read_bytes.sum'},
                         {'name': 'write', 'value': 'lustre.write_bytes.sum'}]
    }]

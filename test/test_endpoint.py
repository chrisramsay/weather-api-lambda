import sys
import urllib2

def http_send_data(server, prepared_data, ignore_last_update=False, headers=None):
    ex_info = []
    success = False

    try:
        prep = server + '?' + prepared_data
        print('get: %s', prep)
        request = urllib2.Request(prep)
        # Add headers if set
        if headers is not None:
            for k,v in headers.items():
                request.add_header(k, v)
        # Check headers are set
        if headers is not None:
            for k in headers.items():
                print('get: %s', request.get_header(k))
        rsp = urllib2.urlopen(request)
        response = rsp.readlines()
        rsp.close()
        for line in response:
            print('rsp: %s', line.strip())
        return False
    except urllib2.HTTPError as ex:
        if sys.version_info >= (2, 7):
            new_ex = '[%d]%s' % (ex.code, ex.reason)
        else:
            new_ex = str(ex)
        ex_info = str(ex.info()).split('\n')
        try:
            for line in ex.readlines():
                line = line.decode('utf-8')
                ex_info.append(re.sub('<.+?>', '', line))
        except Exception:
            pass
    except urllib2.URLError as ex:
        new_ex = str(ex.reason)
    except Exception as ex:
        new_ex = str(ex)
    print('exc: %s', new_ex)
    for extra in ex_info:
        extra = extra.strip()
        if extra:
            print('info: %s', extra)
    return success

if __name__ == "__main__":
    server = 'https://dirtcbrkl8.execute-api.eu-west-1.amazonaws.com/test/station'
    prepared_data = 'temp_dewpt=12.2&wind_ave=0.00&rain=0&rain_day=0&hum_in=62&temp_out=15.1&wind_dir=180&hum_out=83&wind_gust=1.57&temp_apprt=15.8&wind_chill=15.1&tdate=2017-08-10&temp_in=23.1&abs_pressure=1017.4000&ttime=20%3A55%3A50'
    headers = {'x-api-key': 'onsrmmW84U7fdELyNCwkUcq8Dq3DW6D487oyiIZ1'}
    http_send_data(server, prepared_data, False, headers)

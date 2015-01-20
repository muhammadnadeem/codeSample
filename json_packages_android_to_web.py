def package_android_to_web(package_android_format):
    package_web_format = {}
    package_extras = {}
    package_web_format['carrier'] = {'name': package_android_format['carrier']}
    package_web_format['type'] = package_android_format['packageType']
    package_web_format['iso'] = package_android_format['iso']
    package_web_format['currency'] = package_android_format['currency']
    package_web_format['name'] = package_android_format['name']
    package_web_format['url'] = package_android_format['url']
    package_web_format['is_published'] = True

    if 'validity' in package_android_format:
        package_web_format['validity'] = package_android_format['validity']

    if 'recurring_charges' in package_android_format:
        package_web_format['recurring_charges'] = []
        for charge in package_android_format['recurring_charges']:
            rate = charge['rate']
            kind = charge['description']
            pulse = charge['pulse']
            package_web_format['recurring_charges'].append({'rate': rate, 'kind': kind, 'pulse': pulse})

    if 'tax' in package_android_format:
        package_extras['tax'] = package_android_format['tax']

    package_web_format['calculators'] = []
    for counter, calculator in enumerate(package_android_format['calculators']):
        c = dict()

        c['name'] = calculator.get('name', '')
        c['type'] = calculator['type'].upper()

        if 'penalty' in calculator:
            c['penalty'] = calculator['penalty']
        else:
            if c['type'] == 'CALL':
                c['penalty'] = 0.1

        c['pulse'] = calculator['pulse']
        c['rate'] = calculator['rate']
        c['tax'] = calculator.get('tax', 0)

        c['networkfilter'], c['daysfilter'], c['typefilter'], c['isofilter'], c['timefilter'], c['topnumbersfilter'] = \
            [], [], [], [], [], []
        for f in calculator.get('filters', []):
            kind = f['kind'].lower()
            if kind == 'networkfilter':
                networks = f['networks']
                network = ''
                same_network, landline, accept = False, False, False
                for n in networks:
                    if package_android_format['carrier'] == n:
                        same_network = True
                    elif n == 'Landline':
                        landline = True
                accept = f['accept']
                if not same_network and landline and not accept:
                    network = 'onnet+offnet'
                elif not same_network and landline and accept:
                    network = 'landline'
                elif same_network and not landline and not accept:
                    network = 'offnet+landline'
                elif same_network and not landline and accept:
                    network = 'onnet'
                elif same_network and landline and not accept:
                    network = 'offnet'
                elif same_network and landline and accept:
                    network = 'onnet+landline'

                c[kind].append({'network': network})

            if kind == 'isofilter':
                for isofilter in f['iso']:
                    if isofilter != 'PK':
                        isofilter = "ZZ"
                    c[kind].append({'iso': isofilter})
                    break
            elif kind == 'daysfilter':
                c[kind].append({'days': f['days']})
            elif kind == 'timefilter':
                c[kind].append({'start_time': f['start'], 'end_time': f['end']})
            elif kind == 'typefilter':
                c[kind].append({'type': str(f['type'])})
            else:
                c[kind].append({'topnumbers': f['limit']})
        package_web_format['calculators'].append(c)
        c['limiters'] = calculator.get('limiters', [])

    return {'package': package_web_format, 'extras': package_extras}


def main():
    with open("../output/android_json.json") as packages_json_file:
        packages_json_android = json.load(packages_json_file)

    packages_web_format = []

    for package_android_format in packages_json_android['packages']:
        package_web_format = package_android_to_web(package_android_format)
        packages_web_format.append(package_web_format)
        print json.dumps(packages_web_format)


if __name__ == '__main__':
    main()


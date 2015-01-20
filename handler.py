from models import *
from json_packages_android_to_web import package_android_to_web


class FillAppData(webapp2.RequestHandler):
    def import_android_json(self):
        updated_countries = set()

        with open("../output/android_json.json") as json_file:
            json_android = json.load(json_file)

        existing_packages = [pr.name for pr in Package.query().fetch(projection=[Package.name])]
        for package_android_format in json_android['packages'] + json_android['turkPackages']:
            if package_android_format['name'] not in existing_packages:
                package_json = package_android_to_web(package_android_format)

                package = package_json['package']
                carrier = Carrier.get_or_create_by_name(package['iso'], package['carrier']['name'], "15.0")
                pkg = Package(parent=Key(Country, package['iso'], Carrier, carrier.key.id()), version=1,
                              name=package['name'],
                              type=package['type'], pkg_json=package)
                pkg.put()
                updated_countries.add(package['iso'])

        for country in updated_countries:
            Package.update_packages_timestamp(country)

    def get(self):
        self.import_android_json()

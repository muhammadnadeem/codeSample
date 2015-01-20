
# Constants
ALL_COUNTRIES = {"AF": "Afghanistan", "AX": "Aland Islands", "AL": "Albania", "DZ": "Algeria", "AS": "American Samoa",
                 "AD": "Andorra", "AO": "Angola", "AI": "Anguilla", "AQ": "Antarctica", "AG": "Antigua and Barbuda"}


class Country(ndb.Model):
    name = ndb.StringProperty()
    iso = ndb.StringProperty()
    last_modified = ndb.DateTimeProperty(auto_now=True, auto_now_add=True)

    @classmethod
    def add_new_country(cls, iso):
        success, msg = {}, False
        try:
            c = cls(id=iso.upper(), name=ALL_COUNTRIES[iso.upper()], iso=iso.upper())
            c.put()
            success, msg = True, "Country added successfully"
        except Exception as ex:
            msg = ex.message
            print msg
        return success, msg


class Carrier(ndb.Model):
    name = ndb.StringProperty(required=True)
    tax = ndb.FloatProperty(required=True)
    penalty = ndb.FloatProperty(required=True, default=0.1)
    last_modified = ndb.DateTimeProperty(auto_now=True, auto_now_add=True)

    @classmethod
    def get_or_create_by_name(cls, iso, name, tax):
        country = Key(Country, iso.upper()).get()
        if country:
            parent_key = country.key
        else:
            success, msg = Country.add_new_country(iso)
            parent_key = Key(Country, iso.upper())

        carrier = cls.query(Carrier.name == name).get()
        if not carrier:
            carrier = cls(parent=parent_key,
                          name=name,
                          tax=float(tax)
            )
            carrier.put()
        return carrier


class PackageUpdateIndicator(ndb.Model):
    updated_timestamp = ndb.DateTimeProperty(auto_now=True)


# each package will have a parent = Carrier
class Package(ndb.Model):
    version = ndb.IntegerProperty(indexed=True)
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    is_published = ndb.BooleanProperty(default=False)
    is_active = ndb.BooleanProperty(default=True)
    pkg_json = ndb.JsonProperty(compressed=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    modified_at = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def update_packages_timestamp(cls, country_id):
        indicator = PackageUpdateIndicator.query(ancestor=Key(Country, country_id)).get()
        if not indicator:
            indicator = PackageUpdateIndicator(parent=Key(Country, country_id))
        else:
            indicator.updated_timestamp = datetime.now()
        indicator.put()

#!/usr/bin/env python

import datetime
import os
import re
import sys
import time
import urllib2

sys.path.append('%DJANGO_ROOT%')
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from django.db                    import transaction, reset_queries
from blacklist.common.ipcalc    import IPCalc
from blacklist.common.netdata    import NetData
from blacklist.models            import *

registry_data = {
    "ARIN": "ftp://ftp.arin.net/pub/stats/arin/delegated-arin-latest",
    "RIPE": "ftp://ftp.ripe.net/ripe/stats/delegated-ripencc-latest",
    "AfriNIC": "ftp://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest",
    "APNIC": "ftp://ftp.apnic.net/pub/stats/apnic/delegated-apnic-latest",
    "LACNIC": "ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest",
}

countries = [
    ("AF", "AFGHANISTAN"),
    ("AX", "ALAND ISLANDS"),
    ("AL", "ALBANIA"),
    ("DZ", "ALGERIA"),
    ("AS", "AMERICAN SAMOA"),
    ("AD", "ANDORRA"),
    ("AO", "ANGOLA"),
    ("AI", "ANGUILLA"),
    ("AP", "ASIA/PACIFIC REGION"),
    ("AQ", "ANTARCTICA"),
    ("AG", "ANTIGUA AND BARBUDA"),
    ("AR", "ARGENTINA"),
    ("AM", "ARMENIA"),
    ("AW", "ARUBA"),
    ("AU", "AUSTRALIA"),
    ("AT", "AUSTRIA"),
    ("AZ", "AZERBAIJAN"),
    ("BS", "BAHAMAS"),
    ("BH", "BAHRAIN"),
    ("BD", "BANGLADESH"),
    ("BB", "BARBADOS"),
    ("BY", "BELARUS"),
    ("BE", "BELGIUM"),
    ("BZ", "BELIZE"),
    ("BJ", "BENIN"),
    ("BM", "BERMUDA"),
    ("BT", "BHUTAN"),
    ("BO", "BOLIVIA, PLURINATIONAL STATE OF"),
    ("BA", "BOSNIA AND HERZEGOVINA"),
    ("BW", "BOTSWANA"),
    ("BV", "BOUVET ISLAND"),
    ("BR", "BRAZIL"),
    ("IO", "BRITISH INDIAN OCEAN TERRITORY"),
    ("BN", "BRUNEI DARUSSALAM"),
    ("BG", "BULGARIA"),
    ("BF", "BURKINA FASO"),
    ("BI", "BURUNDI"),
    ("KH", "CAMBODIA"),
    ("CM", "CAMEROON"),
    ("CA", "CANADA"),
    ("CV", "CAPE VERDE"),
    ("KY", "CAYMAN ISLANDS"),
    ("CF", "CENTRAL AFRICAN REPUBLIC"),
    ("TD", "CHAD"),
    ("CL", "CHILE"),
    ("CN", "CHINA"),
    ("CX", "CHRISTMAS ISLAND"),
    ("CC", "COCOS (KEELING) ISLANDS"),
    ("CO", "COLOMBIA"),
    ("KM", "COMOROS"),
    ("CG", "CONGO"),
    ("CD", "CONGO, THE DEMOCRATIC REPUBLIC OF THE"),
    ("CK", "COOK ISLANDS"),
    ("CR", "COSTA RICA"),
    ("CI", "COTE D'IVOIRE"),
    ("HR", "CROATIA"),
    ("CU", "CUBA"),
    ("CY", "CYPRUS"),
    ("CZ", "CZECH REPUBLIC"),
    ("DK", "DENMARK"),
    ("DJ", "DJIBOUTI"),
    ("DM", "DOMINICA"),
    ("DO", "DOMINICAN REPUBLIC"),
    ("EC", "ECUADOR"),
    ("EG", "EGYPT"),
    ("SV", "EL SALVADOR"),
    ("GQ", "EQUATORIAL GUINEA"),
    ("ER", "ERITREA"),
    ("EE", "ESTONIA"),
    ("EU", "EUROPEAN UNION"),
    ("ET", "ETHIOPIA"),
    ("FK", "FALKLAND ISLANDS (MALVINAS)"),
    ("FO", "FAROE ISLANDS"),
    ("FJ", "FIJI"),
    ("FI", "FINLAND"),
    ("FR", "FRANCE"),
    ("FX", "FRANCE, METROPOLITAN"),
    ("GF", "FRENCH GUIANA"),
    ("PF", "FRENCH POLYNESIA"),
    ("TF", "FRENCH SOUTHERN TERRITORIES"),
    ("GA", "GABON"),
    ("GM", "GAMBIA"),
    ("GE", "GEORGIA"),
    ("DE", "GERMANY"),
    ("GH", "GHANA"),
    ("GI", "GIBRALTAR"),
    ("GR", "GREECE"),
    ("GL", "GREENLAND"),
    ("GD", "GRENADA"),
    ("GP", "GUADELOUPE"),
    ("GU", "GUAM"),
    ("GT", "GUATEMALA"),
    ("GG", "GUERNSEY"),
    ("GN", "GUINEA"),
    ("GW", "GUINEA-BISSAU"),
    ("GY", "GUYANA"),
    ("HT", "HAITI"),
    ("HM", "HEARD ISLAND AND MCDONALD ISLANDS"),
    ("VA", "VATICAN CITY STATE"),
    ("HN", "HONDURAS"),
    ("HK", "HONG KONG"),
    ("HU", "HUNGARY"),
    ("IS", "ICELAND"),
    ("IN", "INDIA"),
    ("ID", "INDONESIA"),
    ("IR", "IRAN, ISLAMIC REPUBLIC OF"),
    ("IQ", "IRAQ"),
    ("IE", "IRELAND"),
    ("IM", "ISLE OF MAN"),
    ("IL", "ISRAEL"),
    ("IT", "ITALY"),
    ("JM", "JAMAICA"),
    ("JP", "JAPAN"),
    ("JE", "JERSEY"),
    ("JO", "JORDAN"),
    ("KZ", "KAZAKHSTAN"),
    ("KE", "KENYA"),
    ("KI", "KIRIBATI"),
    ("KP", "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF"),
    ("KR", "KOREA, REPUBLIC OF"),
    ("KW", "KUWAIT"),
    ("KG", "KYRGYZSTAN"),
    ("LA", "LAO PEOPLE'S DEMOCRATIC REPUBLIC"),
    ("LV", "LATVIA"),
    ("LB", "LEBANON"),
    ("LS", "LESOTHO"),
    ("LR", "LIBERIA"),
    ("LY", "LIBYAN ARAB JAMAHIRIYA"),
    ("LI", "LIECHTENSTEIN"),
    ("LT", "LITHUANIA"),
    ("LU", "LUXEMBOURG"),
    ("MO", "MACAO"),
    ("MK", "MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF"),
    ("MG", "MADAGASCAR"),
    ("MW", "MALAWI"),
    ("MY", "MALAYSIA"),
    ("MV", "MALDIVES"),
    ("ML", "MALI"),
    ("MT", "MALTA"),
    ("MH", "MARSHALL ISLANDS"),
    ("MQ", "MARTINIQUE"),
    ("MR", "MAURITANIA"),
    ("MU", "MAURITIUS"),
    ("YT", "MAYOTTE"),
    ("MX", "MEXICO"),
    ("FM", "MICRONESIA, FEDERATED STATES OF"),
    ("MD", "MOLDOVA, REPUBLIC OF"),
    ("MC", "MONACO"),
    ("MN", "MONGOLIA"),
    ("ME", "MONTENEGRO"),
    ("MS", "MONTSERRAT"),
    ("MA", "MOROCCO"),
    ("MZ", "MOZAMBIQUE"),
    ("MM", "MYANMAR"),
    ("NA", "NAMIBIA"),
    ("NR", "NAURU"),
    ("NP", "NEPAL"),
    ("NL", "NETHERLANDS"),
    ("AN", "NETHERLANDS ANTILLES"),
    ("NC", "NEW CALEDONIA"),
    ("NZ", "NEW ZEALAND"),
    ("NI", "NICARAGUA"),
    ("NE", "NIGER"),
    ("NG", "NIGERIA"),
    ("NU", "NIUE"),
    ("NF", "NORFOLK ISLAND"),
    ("MP", "NORTHERN MARIANA ISLANDS"),
    ("NO", "NORWAY"),
    ("OM", "OMAN"),
    ("PK", "PAKISTAN"),
    ("PW", "PALAU"),
    ("PS", "PALESTINIAN TERRITORY, OCCUPIED"),
    ("PA", "PANAMA"),
    ("PG", "PAPUA NEW GUINEA"),
    ("PY", "PARAGUAY"),
    ("PE", "PERU"),
    ("PH", "PHILIPPINES"),
    ("PN", "PITCAIRN"),
    ("PL", "POLAND"),
    ("PT", "PORTUGAL"),
    ("PR", "PUERTO RICO"),
    ("QA", "QATAR"),
    ("RE", "REUNION"),
    ("RO", "ROMANIA"),
    ("RU", "RUSSIAN FEDERATION"),
    ("RW", "RWANDA"),
    ("BL", "SAINT BARTHELEMY"),
    ("SH", "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA"),
    ("KN", "SAINT KITTS AND NEVIS"),
    ("LC", "SAINT LUCIA"),
    ("MF", "SAINT MARTIN"),
    ("PM", "SAINT PIERRE AND MIQUELON"),
    ("VC", "SAINT VINCENT AND THE GRENADINES"),
    ("WS", "SAMOA"),
    ("SM", "SAN MARINO"),
    ("ST", "SAO TOME AND PRINCIPE"),
    ("SA", "SAUDI ARABIA"),
    ("SN", "SENEGAL"),
    ("RS", "SERBIA"),
    ("SC", "SEYCHELLES"),
    ("SL", "SIERRA LEONE"),
    ("SG", "SINGAPORE"),
    ("SK", "SLOVAKIA"),
    ("SI", "SLOVENIA"),
    ("SB", "SOLOMON ISLANDS"),
    ("SO", "SOMALIA"),
    ("ZA", "SOUTH AFRICA"),
    ("GS", "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS"),
    ("ES", "SPAIN"),
    ("LK", "SRI LANKA"),
    ("SD", "SUDAN"),
    ("SR", "SURINAME"),
    ("SJ", "SVALBARD AND JAN MAYEN"),
    ("SZ", "SWAZILAND"),
    ("SE", "SWEDEN"),
    ("CH", "SWITZERLAND"),
    ("SY", "SYRIAN ARAB REPUBLIC"),
    ("TW", "TAIWAN, PROVINCE OF CHINA"),
    ("TJ", "TAJIKISTAN"),
    ("TZ", "TANZANIA, UNITED REPUBLIC OF"),
    ("TH", "THAILAND"),
    ("TL", "TIMOR-LESTE"),
    ("TG", "TOGO"),
    ("TK", "TOKELAU"),
    ("TO", "TONGA"),
    ("TT", "TRINIDAD AND TOBAGO"),
    ("TN", "TUNISIA"),
    ("TR", "TURKEY"),
    ("TM", "TURKMENISTAN"),
    ("TC", "TURKS AND CAICOS ISLANDS"),
    ("TV", "TUVALU"),
    ("UG", "UGANDA"),
    ("UA", "UKRAINE"),
    ("AE", "UNITED ARAB EMIRATES"),
    ("GB", "UNITED KINGDOM"),
    ("US", "UNITED STATES"),
    ("UM", "UNITED STATES MINOR OUTLYING ISLANDS"),
    ("UY", "URUGUAY"),
    ("UZ", "UZBEKISTAN"),
    ("VU", "VANUATU"),
    ("VE", "VENEZUELA, BOLIVARIAN REPUBLIC OF"),
    ("VN", "VIET NAM"),
    ("VG", "VIRGIN ISLANDS, BRITISH"),
    ("VI", "VIRGIN ISLANDS, U.S."),
    ("WF", "WALLIS AND FUTUNA"),
    ("EH", "WESTERN SAHARA"),
    ("YE", "YEMEN"),
    ("ZM", "ZAMBIA"),
    ("ZW", "ZIMBABWE"),
]

registries = [
    ["ARIN", "whois.arin.net"],
    ["RIPE", "whois.ripe.net"],
    ["APNIC", "whois.lacnic.net"],
    ["LACNIC", "whois.lacnic.net"],
    ["AfriNIC", "whois.afrinic.net"],
    ["Unknown", "localhost"],
]

error_dir = "%DJANGO_ROOT%/scripts/registry-mgmt/errors"
cache_dir = "%DJANGO_ROOT%/scripts/registry-mgmt/cache"
asn_name_cache = {}
asn_name_cache_file = "%s/asn_name.txt" % (cache_dir)
subnet_asnum_cache = {}
subnet_asnum_cache_file = "%s/subnet_asnum.txt" % (cache_dir)
country_rir_cache = {}

ipcalc = IPCalc()
netdata = NetData()

def prepare_cache():
    if not asn_name_cache and os.path.exists(asn_name_cache_file):
        for line in open(asn_name_cache_file, "r").readlines():
            (asnum, name) = line.split("||")
            asn_name_cache[asnum] = name.strip()

    if not subnet_asnum_cache and os.path.exists(subnet_asnum_cache_file):
        for line in open(subnet_asnum_cache_file, "r").readlines():
            (net, asnum) = line.split("||")
            asnum = asnum.strip()
            if asnum == "-1":
                subnet_asnum_cache[net] = None
            else:
                subnet_asnum_cache[net] = asnum

        for rir in ["ARIN", "RIPE", "AfriNIC", "APNIC", "LACNIC"]:
            for item in cached_registry_data(rir):
                if line.startswith('#'): continue
                t = item.split('|')
                if len(t) != 7: continue
                #if t[2] == 'asn':
                country_rir_cache[t[1]] = rir

def save_cache():
    os.unlink(asn_name_cache_file)
    for k,v in asn_name_cache.items():
        open(asn_name_cache_file, "w").write("%s||%s\n" % (k, v))

    os.unlink(subnet_asnum_cache_file)
    for k,v in subnet_asnum_cache.items():
        open(subnet_asnum_cache_file, "w").write("%s||%s\n" % (k, v))

def cached_get_asn_name(asn):
    try:
        return asn_name_cache[asn]
    except KeyError:
        name = netdata.get_asn_name(asn)
        asn_name_cache[asn] = name
        return asn_name_cache[asn]

def cached_get_subnet_asnum(subnet):
    try:
        return subnet_asnum_cache[subnet]
    except KeyError:
        asn = netdata.get_subnet_asnum(subnet)
        subnet_asnum_cache[subnet] = asn
        return subnet_asnum_cache[subnet]

def cached_registry_data(registry):
    data = []
    if not os.path.exists("%s/%s.txt" % (cache_dir, registry)):
        try:
            fd = open("%s/%s.txt" % (cache_dir, registry), "w")
            for line in urllib2.urlopen(registry_data[registry]).readlines():
                fd.write(line)
                data.append(line)
            fd.close()
        except urllib2.HTTPError:
            print "Failed to retrieve registry data"
            sys.exit(1)
    else:
        data = open("%s/%s.txt" % (cache_dir, registry), "r").readlines()
    return data

@transaction.commit_manually
def import_countries():
    t_start = time.mktime(datetime.datetime.now().timetuple())
    sys.stdout.write("Importing %s countries: " % (len(countries)))
    sys.stdout.flush()
    for country in countries:
        if not country[0] in country_rir_cache: continue
        rir = RIR.objects.get(name=country_rir_cache[country[0]])
        if "," in country[1]:
            (name, additional) = country[1].split(", ")
            cc = Country(
                code=country[0],
                name=name.capitalize(),
                additional=additional.capitalize(),
                rir=rir
            )
            cc.save()
        else:
            cc = Country(
                code=country[0],
                name=country[1].capitalize(),
                rir=rir
            )
            cc.save()
    transaction.commit()
    reset_queries()
    t_end = time.mktime(datetime.datetime.now().timetuple())
    sys.stdout.write("%s seconds\n" % (t_end-t_start))

@transaction.commit_manually
def import_registries():
    t_start = time.mktime(datetime.datetime.now().timetuple())
    sys.stdout.write("Importing %s registries: " % (len(registries)))
    sys.stdout.flush()
    for rir in registries:
        r = RIR(name=rir[0], whois=rir[1])
        r.save()
    transaction.commit()
    reset_queries()
    t_end = time.mktime(datetime.datetime.now().timetuple())
    sys.stdout.write("%s seconds\n" % (t_end-t_start))

def prepare_asnum_data(registry):
    t_start = time.mktime(datetime.datetime.now().timetuple())
    tot_asnum = 0
    all_asnums = []
    db_asnums = []
    for asn in ASNum.objects.all().iterator():
        db_asnums.append(asn.asnum)
    sys.stdout.write("* preparing asnums: ")
    sys.stdout.flush()
    rir = RIR.objects.get(name=registry)
    for line in cached_registry_data(registry):
        if line.startswith("#"):
            continue
        t = line.split("|")
        if t[5] == 'summary\n': continue
        if t[2] == "asn":
            if t[3] in db_asnums:
                continue

            country = Country.objects.get(code=t[1])

            try:
                regdate=datetime.datetime.strptime(t[5], "%Y%m%d")
            except:
                regdate=datetime.datetime.strptime("19700101", "%Y%m%d")

            all_asnums.append([t[3], cached_get_asn_name(t[3]), country, rir, regdate])
            tot_asnum += 1
    t_end = time.mktime(datetime.datetime.now().timetuple())
    print "%s found, %s seconds" % (tot_asnum, int(t_end - t_start))
    return all_asnums

@transaction.commit_manually
def import_asnum_data(all_asnums):
    t_start = time.mktime(datetime.datetime.now().timetuple())
    sys.stdout.write("* commiting asnums to database: ")
    sys.stdout.flush()
    for asn in all_asnums:
            asnum = ASNum(
                asnum=asn[0],
                name=asn[1],
                country=asn[2],
                rir=asn[3],
                regdate=asn[4],
            )
            asnum.save()
    transaction.commit()
    reset_queries()
    t_end = time.mktime(datetime.datetime.now().timetuple())
    print "%s seconds" % (int(t_end - t_start))

def prepare_subnet_data(registry):
    t_start = time.mktime(datetime.datetime.now().timetuple())
    db_asnums = {}
    all_subnets = []
    db_subnets = []
    tot_subnet = 0
    sys.stdout.write("* preparing subnets: ")
    sys.stdout.flush()
    for asnum in ASNum.objects.all().iterator():
        db_asnums[asnum.asnum] = asnum
    for subnet in Subnet.objects.all().iterator():
        db_subnets.append(subnet.subnet)
    rir = RIR.objects.get(name=registry)
    for line in cached_registry_data(registry):
        if line.startswith("#"):
            continue
        t = line.split("|")
        if t[5] == 'summary\n': continue

        if t[2] in ["ipv4", "ipv6"]:
            if "." in t[3]:
                af = 4
            else:
                af = 6

            country = Country.objects.get(code=t[1])

            asn = cached_get_subnet_asnum(t[3])
            country = Country.objects.get(code=t[1])

            try:
                regdate=datetime.datetime.strptime(t[5], "%Y%m%d")
            except:
                regdate=datetime.datetime.strptime("19700101", "%Y%m%d")

            if asn:
                try:
                    asnum = db_asnums[asn]
                except KeyError:
                    asnum = ASNum(
                        asnum=asn,
                        name=cached_get_asn_name(asn),
                        country=country,
                        rir=rir,
                        regdate=regdate

                    )
                    asnum.save()
                    db_asnums[asn] = asnum
            else:
                asnum = None

            no_mask = False
            if af == 4:
                try:
                    mask = ipcalc.iptobit[int(t[4])]
                except:
                    no_mask = True
            else:
                mask = int(t[4])

            subnets = []
            if not no_mask:
                net_first = ipcalc.dqtoi(t[3])
                #if net_first in db_subnets:
                #    continue

                if af == 4:
                    net_last = net_first+int(t[4])
                else:
                    net_last = net_first+ipcalc.size("%s/%s" % (t[3], t[4]))
                subnets.append([net_first, net_last, mask])
            else:
                if af == 4:
                    for net in ipcalc.aggregates(ipcalc.dqtoi(t[3]), int(t[4]), []):
                        net_first = net[0]
                        #if net_first in db_subnets:
                        #    continue

                        net_last = net_first + ipcalc.bittoip[net[1]]
                        subnets.append([net_first, net_last, net[1]])

            for net in subnets:
                all_subnets.append([net[0], net[1], net[2], asnum, af, country, regdate])
                tot_subnet += 1

    t_end = time.mktime(datetime.datetime.now().timetuple())
    print "%s found, %s seconds" % (tot_subnet, int(t_end - t_start))
    return all_subnets

@transaction.commit_manually
def import_subnet_data(all_subnets, registry):
    t_start = time.mktime(datetime.datetime.now().timetuple())
    sys.stdout.write("* commiting subnets to database: ")
    sys.stdout.flush()
    rir = RIR.objects.get(name=registry)
    for net in all_subnets:
        subnet = Subnet(
            subnet=net[0],
            last=net[1],
            mask=net[2],
            asnum=net[3],
            af=net[4],
            country=net[5],
            regdate=net[6],
            rir=rir,
        )
        subnet.save()
    transaction.commit()
    reset_queries()
    t_end = time.mktime(datetime.datetime.now().timetuple())
    print "%s seconds" % (int(t_end - t_start))

if __name__ == "__main__":
    prepare_cache()
    sys.setcheckinterval(1000000)
    # eww, dirty, this is being done from a south migration
    # import_registries()
    import_countries()
    for rir in ["ARIN", "RIPE", "AfriNIC", "APNIC", "LACNIC"]:
        print "Importing %s data" % (rir)
        import_asnum_data(prepare_asnum_data(rir))
        import_subnet_data(prepare_subnet_data(rir), rir)
    save_cache()

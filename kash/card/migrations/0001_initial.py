# Generated by Django 3.1.1 on 2022-02-28 16:46

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("kash_user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VirtualCard",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(blank=True, max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("nickname", models.CharField(max_length=255)),
                ("category", models.CharField(blank=True, max_length=255)),
                ("last_4", models.CharField(blank=True, max_length=4)),
                (
                    "provider_name",
                    models.CharField(
                        choices=[("rave", "Rave"), ("dummy", "Dummy")],
                        default="rave",
                        max_length=20,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kash_user.userprofile",
                    ),
                ),
            ],
            options={"abstract": False, "db_table": "kash_virtualcard"},
        ),
        migrations.CreateModel(
            name="WithdrawalHistory",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("txn_ref", models.CharField(blank=True, max_length=255)),
                (
                    "amount_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[
                            ("XUA", "ADB Unit of Account"),
                            ("AFN", "Afghani"),
                            ("DZD", "Algerian Dinar"),
                            ("ARS", "Argentine Peso"),
                            ("AMD", "Armenian Dram"),
                            ("AWG", "Aruban Guilder"),
                            ("AUD", "Australian Dollar"),
                            ("AZN", "Azerbaijanian Manat"),
                            ("BSD", "Bahamian Dollar"),
                            ("BHD", "Bahraini Dinar"),
                            ("THB", "Baht"),
                            ("PAB", "Balboa"),
                            ("BBD", "Barbados Dollar"),
                            ("BYN", "Belarussian Ruble"),
                            ("BYR", "Belarussian Ruble"),
                            ("BZD", "Belize Dollar"),
                            (
                                "BMD",
                                "Bermudian Dollar (customarily known as Bermuda Dollar)",
                            ),
                            ("BTN", "Bhutanese ngultrum"),
                            ("VEF", "Bolivar Fuerte"),
                            ("BOB", "Boliviano"),
                            (
                                "XBA",
                                "Bond Markets Units European Composite Unit (EURCO)",
                            ),
                            ("BRL", "Brazilian Real"),
                            ("BND", "Brunei Dollar"),
                            ("BGN", "Bulgarian Lev"),
                            ("BIF", "Burundi Franc"),
                            ("XOF", "CFA Franc BCEAO"),
                            ("XAF", "CFA franc BEAC"),
                            ("XPF", "CFP Franc"),
                            ("CAD", "Canadian Dollar"),
                            ("CVE", "Cape Verde Escudo"),
                            ("KYD", "Cayman Islands Dollar"),
                            ("CLP", "Chilean peso"),
                            ("XTS", "Codes specifically reserved for testing purposes"),
                            ("COP", "Colombian peso"),
                            ("KMF", "Comoro Franc"),
                            ("CDF", "Congolese franc"),
                            ("BAM", "Convertible Marks"),
                            ("NIO", "Cordoba Oro"),
                            ("CRC", "Costa Rican Colon"),
                            ("HRK", "Croatian Kuna"),
                            ("CUP", "Cuban Peso"),
                            ("CUC", "Cuban convertible peso"),
                            ("CZK", "Czech Koruna"),
                            ("GMD", "Dalasi"),
                            ("DKK", "Danish Krone"),
                            ("MKD", "Denar"),
                            ("DJF", "Djibouti Franc"),
                            ("STD", "Dobra"),
                            ("DOP", "Dominican Peso"),
                            ("VND", "Dong"),
                            ("XCD", "East Caribbean Dollar"),
                            ("EGP", "Egyptian Pound"),
                            ("SVC", "El Salvador Colon"),
                            ("ETB", "Ethiopian Birr"),
                            ("EUR", "Euro"),
                            ("XBB", "European Monetary Unit (E.M.U.-6)"),
                            ("XBD", "European Unit of Account 17(E.U.A.-17)"),
                            ("XBC", "European Unit of Account 9(E.U.A.-9)"),
                            ("FKP", "Falkland Islands Pound"),
                            ("FJD", "Fiji Dollar"),
                            ("HUF", "Forint"),
                            ("GHS", "Ghana Cedi"),
                            ("GIP", "Gibraltar Pound"),
                            ("XAU", "Gold"),
                            ("XFO", "Gold-Franc"),
                            ("PYG", "Guarani"),
                            ("GNF", "Guinea Franc"),
                            ("GYD", "Guyana Dollar"),
                            ("HTG", "Haitian gourde"),
                            ("HKD", "Hong Kong Dollar"),
                            ("UAH", "Hryvnia"),
                            ("ISK", "Iceland Krona"),
                            ("INR", "Indian Rupee"),
                            ("IRR", "Iranian Rial"),
                            ("IQD", "Iraqi Dinar"),
                            ("IMP", "Isle of Man Pound"),
                            ("JMD", "Jamaican Dollar"),
                            ("JOD", "Jordanian Dinar"),
                            ("KES", "Kenyan Shilling"),
                            ("PGK", "Kina"),
                            ("LAK", "Kip"),
                            ("KWD", "Kuwaiti Dinar"),
                            ("AOA", "Kwanza"),
                            ("MMK", "Kyat"),
                            ("GEL", "Lari"),
                            ("LVL", "Latvian Lats"),
                            ("LBP", "Lebanese Pound"),
                            ("ALL", "Lek"),
                            ("HNL", "Lempira"),
                            ("SLL", "Leone"),
                            ("LSL", "Lesotho loti"),
                            ("LRD", "Liberian Dollar"),
                            ("LYD", "Libyan Dinar"),
                            ("SZL", "Lilangeni"),
                            ("LTL", "Lithuanian Litas"),
                            ("MGA", "Malagasy Ariary"),
                            ("MWK", "Malawian Kwacha"),
                            ("MYR", "Malaysian Ringgit"),
                            ("TMM", "Manat"),
                            ("MUR", "Mauritius Rupee"),
                            ("MZN", "Metical"),
                            ("MXV", "Mexican Unidad de Inversion (UDI)"),
                            ("MXN", "Mexican peso"),
                            ("MDL", "Moldovan Leu"),
                            ("MAD", "Moroccan Dirham"),
                            ("BOV", "Mvdol"),
                            ("NGN", "Naira"),
                            ("ERN", "Nakfa"),
                            ("NAD", "Namibian Dollar"),
                            ("NPR", "Nepalese Rupee"),
                            ("ANG", "Netherlands Antillian Guilder"),
                            ("ILS", "New Israeli Sheqel"),
                            ("RON", "New Leu"),
                            ("TWD", "New Taiwan Dollar"),
                            ("NZD", "New Zealand Dollar"),
                            ("KPW", "North Korean Won"),
                            ("NOK", "Norwegian Krone"),
                            ("PEN", "Nuevo Sol"),
                            ("MRO", "Ouguiya"),
                            ("TOP", "Paanga"),
                            ("PKR", "Pakistan Rupee"),
                            ("XPD", "Palladium"),
                            ("MOP", "Pataca"),
                            ("PHP", "Philippine Peso"),
                            ("XPT", "Platinum"),
                            ("GBP", "Pound Sterling"),
                            ("BWP", "Pula"),
                            ("QAR", "Qatari Rial"),
                            ("GTQ", "Quetzal"),
                            ("ZAR", "Rand"),
                            ("OMR", "Rial Omani"),
                            ("KHR", "Riel"),
                            ("MVR", "Rufiyaa"),
                            ("IDR", "Rupiah"),
                            ("RUB", "Russian Ruble"),
                            ("RWF", "Rwanda Franc"),
                            ("XDR", "SDR"),
                            ("SHP", "Saint Helena Pound"),
                            ("SAR", "Saudi Riyal"),
                            ("RSD", "Serbian Dinar"),
                            ("SCR", "Seychelles Rupee"),
                            ("XAG", "Silver"),
                            ("SGD", "Singapore Dollar"),
                            ("SBD", "Solomon Islands Dollar"),
                            ("KGS", "Som"),
                            ("SOS", "Somali Shilling"),
                            ("TJS", "Somoni"),
                            ("SSP", "South Sudanese Pound"),
                            ("LKR", "Sri Lanka Rupee"),
                            ("XSU", "Sucre"),
                            ("SDG", "Sudanese Pound"),
                            ("SRD", "Surinam Dollar"),
                            ("SEK", "Swedish Krona"),
                            ("CHF", "Swiss Franc"),
                            ("SYP", "Syrian Pound"),
                            ("BDT", "Taka"),
                            ("WST", "Tala"),
                            ("TZS", "Tanzanian Shilling"),
                            ("KZT", "Tenge"),
                            (
                                "XXX",
                                "The codes assigned for transactions where no currency is involved",
                            ),
                            ("TTD", "Trinidad and Tobago Dollar"),
                            ("MNT", "Tugrik"),
                            ("TND", "Tunisian Dinar"),
                            ("TRY", "Turkish Lira"),
                            ("TMT", "Turkmenistan New Manat"),
                            ("TVD", "Tuvalu dollar"),
                            ("AED", "UAE Dirham"),
                            ("XFU", "UIC-Franc"),
                            ("USD", "US Dollar"),
                            ("USN", "US Dollar (Next day)"),
                            ("UGX", "Uganda Shilling"),
                            ("CLF", "Unidad de Fomento"),
                            ("COU", "Unidad de Valor Real"),
                            ("UYI", "Uruguay Peso en Unidades Indexadas (URUIURUI)"),
                            ("UYU", "Uruguayan peso"),
                            ("UZS", "Uzbekistan Sum"),
                            ("VUV", "Vatu"),
                            ("CHE", "WIR Euro"),
                            ("CHW", "WIR Franc"),
                            ("KRW", "Won"),
                            ("YER", "Yemeni Rial"),
                            ("JPY", "Yen"),
                            ("CNY", "Yuan Renminbi"),
                            ("ZMK", "Zambian Kwacha"),
                            ("ZMW", "Zambian Kwacha"),
                            ("ZWD", "Zimbabwe Dollar A/06"),
                            ("ZWN", "Zimbabwe dollar A/08"),
                            ("ZWL", "Zimbabwe dollar A/09"),
                            ("PLN", "Zloty"),
                        ],
                        default="XOF",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "amount",
                    djmoney.models.fields.MoneyField(
                        decimal_places=2, default_currency="XOF", max_digits=17
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("paid-out", "Paid Out"),
                            ("failed", "Failed"),
                            ("pending", "Pending"),
                            ("withdrawn", "Withdrawn"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kash_card.virtualcard",
                    ),
                ),
            ],
            options={"abstract": False, "db_table": "kash_withdrawalhistory"},
        ),
        migrations.CreateModel(
            name="FundingHistory",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("txn_ref", models.CharField(max_length=255, unique=True)),
                (
                    "amount_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[
                            ("XUA", "ADB Unit of Account"),
                            ("AFN", "Afghani"),
                            ("DZD", "Algerian Dinar"),
                            ("ARS", "Argentine Peso"),
                            ("AMD", "Armenian Dram"),
                            ("AWG", "Aruban Guilder"),
                            ("AUD", "Australian Dollar"),
                            ("AZN", "Azerbaijanian Manat"),
                            ("BSD", "Bahamian Dollar"),
                            ("BHD", "Bahraini Dinar"),
                            ("THB", "Baht"),
                            ("PAB", "Balboa"),
                            ("BBD", "Barbados Dollar"),
                            ("BYN", "Belarussian Ruble"),
                            ("BYR", "Belarussian Ruble"),
                            ("BZD", "Belize Dollar"),
                            (
                                "BMD",
                                "Bermudian Dollar (customarily known as Bermuda Dollar)",
                            ),
                            ("BTN", "Bhutanese ngultrum"),
                            ("VEF", "Bolivar Fuerte"),
                            ("BOB", "Boliviano"),
                            (
                                "XBA",
                                "Bond Markets Units European Composite Unit (EURCO)",
                            ),
                            ("BRL", "Brazilian Real"),
                            ("BND", "Brunei Dollar"),
                            ("BGN", "Bulgarian Lev"),
                            ("BIF", "Burundi Franc"),
                            ("XOF", "CFA Franc BCEAO"),
                            ("XAF", "CFA franc BEAC"),
                            ("XPF", "CFP Franc"),
                            ("CAD", "Canadian Dollar"),
                            ("CVE", "Cape Verde Escudo"),
                            ("KYD", "Cayman Islands Dollar"),
                            ("CLP", "Chilean peso"),
                            ("XTS", "Codes specifically reserved for testing purposes"),
                            ("COP", "Colombian peso"),
                            ("KMF", "Comoro Franc"),
                            ("CDF", "Congolese franc"),
                            ("BAM", "Convertible Marks"),
                            ("NIO", "Cordoba Oro"),
                            ("CRC", "Costa Rican Colon"),
                            ("HRK", "Croatian Kuna"),
                            ("CUP", "Cuban Peso"),
                            ("CUC", "Cuban convertible peso"),
                            ("CZK", "Czech Koruna"),
                            ("GMD", "Dalasi"),
                            ("DKK", "Danish Krone"),
                            ("MKD", "Denar"),
                            ("DJF", "Djibouti Franc"),
                            ("STD", "Dobra"),
                            ("DOP", "Dominican Peso"),
                            ("VND", "Dong"),
                            ("XCD", "East Caribbean Dollar"),
                            ("EGP", "Egyptian Pound"),
                            ("SVC", "El Salvador Colon"),
                            ("ETB", "Ethiopian Birr"),
                            ("EUR", "Euro"),
                            ("XBB", "European Monetary Unit (E.M.U.-6)"),
                            ("XBD", "European Unit of Account 17(E.U.A.-17)"),
                            ("XBC", "European Unit of Account 9(E.U.A.-9)"),
                            ("FKP", "Falkland Islands Pound"),
                            ("FJD", "Fiji Dollar"),
                            ("HUF", "Forint"),
                            ("GHS", "Ghana Cedi"),
                            ("GIP", "Gibraltar Pound"),
                            ("XAU", "Gold"),
                            ("XFO", "Gold-Franc"),
                            ("PYG", "Guarani"),
                            ("GNF", "Guinea Franc"),
                            ("GYD", "Guyana Dollar"),
                            ("HTG", "Haitian gourde"),
                            ("HKD", "Hong Kong Dollar"),
                            ("UAH", "Hryvnia"),
                            ("ISK", "Iceland Krona"),
                            ("INR", "Indian Rupee"),
                            ("IRR", "Iranian Rial"),
                            ("IQD", "Iraqi Dinar"),
                            ("IMP", "Isle of Man Pound"),
                            ("JMD", "Jamaican Dollar"),
                            ("JOD", "Jordanian Dinar"),
                            ("KES", "Kenyan Shilling"),
                            ("PGK", "Kina"),
                            ("LAK", "Kip"),
                            ("KWD", "Kuwaiti Dinar"),
                            ("AOA", "Kwanza"),
                            ("MMK", "Kyat"),
                            ("GEL", "Lari"),
                            ("LVL", "Latvian Lats"),
                            ("LBP", "Lebanese Pound"),
                            ("ALL", "Lek"),
                            ("HNL", "Lempira"),
                            ("SLL", "Leone"),
                            ("LSL", "Lesotho loti"),
                            ("LRD", "Liberian Dollar"),
                            ("LYD", "Libyan Dinar"),
                            ("SZL", "Lilangeni"),
                            ("LTL", "Lithuanian Litas"),
                            ("MGA", "Malagasy Ariary"),
                            ("MWK", "Malawian Kwacha"),
                            ("MYR", "Malaysian Ringgit"),
                            ("TMM", "Manat"),
                            ("MUR", "Mauritius Rupee"),
                            ("MZN", "Metical"),
                            ("MXV", "Mexican Unidad de Inversion (UDI)"),
                            ("MXN", "Mexican peso"),
                            ("MDL", "Moldovan Leu"),
                            ("MAD", "Moroccan Dirham"),
                            ("BOV", "Mvdol"),
                            ("NGN", "Naira"),
                            ("ERN", "Nakfa"),
                            ("NAD", "Namibian Dollar"),
                            ("NPR", "Nepalese Rupee"),
                            ("ANG", "Netherlands Antillian Guilder"),
                            ("ILS", "New Israeli Sheqel"),
                            ("RON", "New Leu"),
                            ("TWD", "New Taiwan Dollar"),
                            ("NZD", "New Zealand Dollar"),
                            ("KPW", "North Korean Won"),
                            ("NOK", "Norwegian Krone"),
                            ("PEN", "Nuevo Sol"),
                            ("MRO", "Ouguiya"),
                            ("TOP", "Paanga"),
                            ("PKR", "Pakistan Rupee"),
                            ("XPD", "Palladium"),
                            ("MOP", "Pataca"),
                            ("PHP", "Philippine Peso"),
                            ("XPT", "Platinum"),
                            ("GBP", "Pound Sterling"),
                            ("BWP", "Pula"),
                            ("QAR", "Qatari Rial"),
                            ("GTQ", "Quetzal"),
                            ("ZAR", "Rand"),
                            ("OMR", "Rial Omani"),
                            ("KHR", "Riel"),
                            ("MVR", "Rufiyaa"),
                            ("IDR", "Rupiah"),
                            ("RUB", "Russian Ruble"),
                            ("RWF", "Rwanda Franc"),
                            ("XDR", "SDR"),
                            ("SHP", "Saint Helena Pound"),
                            ("SAR", "Saudi Riyal"),
                            ("RSD", "Serbian Dinar"),
                            ("SCR", "Seychelles Rupee"),
                            ("XAG", "Silver"),
                            ("SGD", "Singapore Dollar"),
                            ("SBD", "Solomon Islands Dollar"),
                            ("KGS", "Som"),
                            ("SOS", "Somali Shilling"),
                            ("TJS", "Somoni"),
                            ("SSP", "South Sudanese Pound"),
                            ("LKR", "Sri Lanka Rupee"),
                            ("XSU", "Sucre"),
                            ("SDG", "Sudanese Pound"),
                            ("SRD", "Surinam Dollar"),
                            ("SEK", "Swedish Krona"),
                            ("CHF", "Swiss Franc"),
                            ("SYP", "Syrian Pound"),
                            ("BDT", "Taka"),
                            ("WST", "Tala"),
                            ("TZS", "Tanzanian Shilling"),
                            ("KZT", "Tenge"),
                            (
                                "XXX",
                                "The codes assigned for transactions where no currency is involved",
                            ),
                            ("TTD", "Trinidad and Tobago Dollar"),
                            ("MNT", "Tugrik"),
                            ("TND", "Tunisian Dinar"),
                            ("TRY", "Turkish Lira"),
                            ("TMT", "Turkmenistan New Manat"),
                            ("TVD", "Tuvalu dollar"),
                            ("AED", "UAE Dirham"),
                            ("XFU", "UIC-Franc"),
                            ("USD", "US Dollar"),
                            ("USN", "US Dollar (Next day)"),
                            ("UGX", "Uganda Shilling"),
                            ("CLF", "Unidad de Fomento"),
                            ("COU", "Unidad de Valor Real"),
                            ("UYI", "Uruguay Peso en Unidades Indexadas (URUIURUI)"),
                            ("UYU", "Uruguayan peso"),
                            ("UZS", "Uzbekistan Sum"),
                            ("VUV", "Vatu"),
                            ("CHE", "WIR Euro"),
                            ("CHW", "WIR Franc"),
                            ("KRW", "Won"),
                            ("YER", "Yemeni Rial"),
                            ("JPY", "Yen"),
                            ("CNY", "Yuan Renminbi"),
                            ("ZMK", "Zambian Kwacha"),
                            ("ZMW", "Zambian Kwacha"),
                            ("ZWD", "Zimbabwe Dollar A/06"),
                            ("ZWN", "Zimbabwe dollar A/08"),
                            ("ZWL", "Zimbabwe dollar A/09"),
                            ("PLN", "Zloty"),
                        ],
                        default="USD",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "amount",
                    djmoney.models.fields.MoneyField(
                        decimal_places=2, default_currency="USD", max_digits=17
                    ),
                ),
                ("status", models.CharField(max_length=15)),
                ("retries", models.PositiveIntegerField(default=0)),
                ("is_funding", models.BooleanField(default=False)),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="kash_card.virtualcard",
                    ),
                ),
            ],
            options={"abstract": False, "db_table": "kash_fundinghistory"},
        ),
    ]

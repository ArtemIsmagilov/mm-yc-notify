EXPAND_DICT = {
    "app": "all",
    "acting_user": "all",
    "acting_user_access_token": "all",
    "locale": "all",
    "channel": "all",
    "channel_member": "all",
    "team": "all",
    "team_member": "all",
    "post": "all",
    "root_post": "all",
    "user": "all",
    "oauth2_app": "all",
    "oauth2_user": "all",
}

UTCs = (
    {'label': '(UTC+11:00) Antarctica/Casey', 'value': 'Antarctica/Casey'},
    {'label': '(UTC-05:00) America/North_Dakota/Center', 'value': 'America/North_Dakota/Center'},
    {'label': '(UTC+03:00) Europe/Moscow', 'value': 'Europe/Moscow'},
    {'label': '(UTC+07:00) Asia/Jakarta', 'value': 'Asia/Jakarta'},
    {'label': '(UTC+04:00) Europe/Samara', 'value': 'Europe/Samara'},
    {'label': '(UTC+02:00) Africa/Tripoli', 'value': 'Africa/Tripoli'},
    {'label': '(UTC-03:00) America/Glace_Bay', 'value': 'America/Glace_Bay'},
    {'label': '(UTC-04:00) America/Dominica', 'value': 'America/Dominica'},
    {'label': '(UTC+08:00) Asia/Macau', 'value': 'Asia/Macau'},
    {'label': '(UTC-04:00) America/St_Thomas', 'value': 'America/St_Thomas'},
    {'label': '(UTC+00:00) GMT', 'value': 'GMT'}, {'label': '(UTC+13:00) Pacific/Apia', 'value': 'Pacific/Apia'},
    {'label': '(UTC-04:00) America/Marigot', 'value': 'America/Marigot'},
    {'label': '(UTC-03:00) Canada/Atlantic', 'value': 'Canada/Atlantic'},
    {'label': '(UTC+02:00) Europe/Kaliningrad', 'value': 'Europe/Kaliningrad'},
    {'label': '(UTC-03:00) America/Punta_Arenas', 'value': 'America/Punta_Arenas'},
    {'label': '(UTC-04:00) America/Tortola', 'value': 'America/Tortola'},
    {'label': '(UTC+03:00) Asia/Damascus', 'value': 'Asia/Damascus'},
    {'label': '(UTC-10:00) Pacific/Honolulu', 'value': 'Pacific/Honolulu'},
    {'label': '(UTC-05:00) America/Cayman', 'value': 'America/Cayman'},
    {'label': '(UTC+00:00) Africa/Ouagadougou', 'value': 'Africa/Ouagadougou'},
    {'label': '(UTC+00:00) Africa/Dakar', 'value': 'Africa/Dakar'},
    {'label': '(UTC+03:00) Europe/Vilnius', 'value': 'Europe/Vilnius'},
    {'label': '(UTC+02:00) Africa/Kigali', 'value': 'Africa/Kigali'},
    {'label': '(UTC+00:00) Africa/Conakry', 'value': 'Africa/Conakry'},
    {'label': '(UTC+03:00) Europe/Sofia', 'value': 'Europe/Sofia'},
    {'label': '(UTC-06:00) America/Tegucigalpa', 'value': 'America/Tegucigalpa'},
    {'label': '(UTC+02:00) Europe/Copenhagen', 'value': 'Europe/Copenhagen'},
    {'label': '(UTC-04:00) America/Kralendijk', 'value': 'America/Kralendijk'},
    {'label': '(UTC+13:00) Pacific/Kanton', 'value': 'Pacific/Kanton'},
    {'label': '(UTC+03:00) Africa/Djibouti', 'value': 'Africa/Djibouti'},
    {'label': '(UTC+06:00) Asia/Omsk', 'value': 'Asia/Omsk'},
    {'label': '(UTC-08:00) America/Nome', 'value': 'America/Nome'},
    {'label': '(UTC+00:00) Africa/Banjul', 'value': 'Africa/Banjul'},
    {'label': '(UTC+05:00) Asia/Oral', 'value': 'Asia/Oral'},
    {'label': '(UTC-06:00) America/Merida', 'value': 'America/Merida'},
    {'label': '(UTC-03:00) America/Sao_Paulo', 'value': 'America/Sao_Paulo'},
    {'label': '(UTC+09:00) Asia/Chita', 'value': 'Asia/Chita'},
    {'label': '(UTC-09:00) America/Adak', 'value': 'America/Adak'},
    {'label': '(UTC-05:00) America/Lima', 'value': 'America/Lima'},
    {'label': '(UTC+01:00) Africa/Brazzaville', 'value': 'Africa/Brazzaville'},
    {'label': '(UTC+04:00) Europe/Astrakhan', 'value': 'Europe/Astrakhan'},
    {'label': '(UTC+06:30) Indian/Cocos', 'value': 'Indian/Cocos'},
    {'label': '(UTC-04:00) America/Martinique', 'value': 'America/Martinique'},
    {'label': '(UTC+13:45) Pacific/Chatham', 'value': 'Pacific/Chatham'},
    {'label': '(UTC+05:30) Asia/Colombo', 'value': 'Asia/Colombo'},
    {'label': '(UTC-05:00) America/Menominee', 'value': 'America/Menominee'},
    {'label': '(UTC+05:00) Indian/Kerguelen', 'value': 'Indian/Kerguelen'},
    {'label': '(UTC+10:00) Pacific/Chuuk', 'value': 'Pacific/Chuuk'},
    {'label': '(UTC+02:00) Europe/Malta', 'value': 'Europe/Malta'},
    {'label': '(UTC+08:00) Asia/Choibalsan', 'value': 'Asia/Choibalsan'},
    {'label': '(UTC-05:00) America/Indiana/Knox', 'value': 'America/Indiana/Knox'},
    {'label': '(UTC+01:00) Africa/Douala', 'value': 'Africa/Douala'},
    {'label': '(UTC-04:00) America/Indiana/Marengo', 'value': 'America/Indiana/Marengo'},
    {'label': '(UTC-11:00) Pacific/Niue', 'value': 'Pacific/Niue'},
    {'label': '(UTC+11:00) Pacific/Guadalcanal', 'value': 'Pacific/Guadalcanal'},
    {'label': '(UTC-03:00) America/Argentina/Catamarca', 'value': 'America/Argentina/Catamarca'},
    {'label': '(UTC+12:00) Pacific/Nauru', 'value': 'Pacific/Nauru'},
    {'label': '(UTC+03:00) Asia/Nicosia', 'value': 'Asia/Nicosia'},
    {'label': '(UTC-03:00) America/Argentina/Rio_Gallegos', 'value': 'America/Argentina/Rio_Gallegos'},
    {'label': '(UTC+02:00) Asia/Hebron', 'value': 'Asia/Hebron'},
    {'label': '(UTC+08:00) Asia/Kuching', 'value': 'Asia/Kuching'},
    {'label': '(UTC+03:00) Africa/Mogadishu', 'value': 'Africa/Mogadishu'},
    {'label': '(UTC+03:00) Europe/Kirov', 'value': 'Europe/Kirov'},
    {'label': '(UTC-04:00) US/Eastern', 'value': 'US/Eastern'},
    {'label': '(UTC-02:30) Canada/Newfoundland', 'value': 'Canada/Newfoundland'},
    {'label': '(UTC-07:00) America/Creston', 'value': 'America/Creston'},
    {'label': '(UTC-04:00) America/Kentucky/Monticello', 'value': 'America/Kentucky/Monticello'},
    {'label': '(UTC-03:00) Atlantic/Bermuda', 'value': 'Atlantic/Bermuda'},
    {'label': '(UTC-03:00) America/Araguaina', 'value': 'America/Araguaina'},
    {'label': '(UTC+01:00) Africa/Ndjamena', 'value': 'Africa/Ndjamena'},
    {'label': '(UTC-03:00) Antarctica/Palmer', 'value': 'Antarctica/Palmer'},
    {'label': '(UTC+08:00) Asia/Irkutsk', 'value': 'Asia/Irkutsk'},
    {'label': '(UTC+08:00) Asia/Hong_Kong', 'value': 'Asia/Hong_Kong'},
    {'label': '(UTC+01:00) Africa/Tunis', 'value': 'Africa/Tunis'},
    {'label': '(UTC-03:00) America/Paramaribo', 'value': 'America/Paramaribo'},
    {'label': '(UTC-08:00) US/Alaska', 'value': 'US/Alaska'},
    {'label': '(UTC+12:00) Pacific/Kwajalein', 'value': 'Pacific/Kwajalein'},
    {'label': '(UTC+00:00) Africa/Monrovia', 'value': 'Africa/Monrovia'},
    {'label': '(UTC+05:00) Asia/Tashkent', 'value': 'Asia/Tashkent'},
    {'label': '(UTC+01:00) Atlantic/Faroe', 'value': 'Atlantic/Faroe'},
    {'label': '(UTC+04:00) Europe/Ulyanovsk', 'value': 'Europe/Ulyanovsk'},
    {'label': '(UTC-02:00) Atlantic/South_Georgia', 'value': 'Atlantic/South_Georgia'},
    {'label': '(UTC-05:00) America/Ojinaga', 'value': 'America/Ojinaga'},
    {'label': '(UTC-04:00) America/St_Lucia', 'value': 'America/St_Lucia'},
    {'label': '(UTC+10:00) Pacific/Port_Moresby', 'value': 'Pacific/Port_Moresby'},
    {'label': '(UTC+02:00) Africa/Johannesburg', 'value': 'Africa/Johannesburg'},
    {'label': '(UTC+01:00) Africa/Luanda', 'value': 'Africa/Luanda'},
    {'label': '(UTC-04:00) America/Boa_Vista', 'value': 'America/Boa_Vista'},
    {'label': '(UTC+05:45) Asia/Kathmandu', 'value': 'Asia/Kathmandu'},
    {'label': '(UTC+09:00) Asia/Pyongyang', 'value': 'Asia/Pyongyang'},
    {'label': '(UTC-03:00) America/Fortaleza', 'value': 'America/Fortaleza'},
    {'label': '(UTC-03:00) America/Asuncion', 'value': 'America/Asuncion'},
    {'label': '(UTC-08:00) America/Juneau', 'value': 'America/Juneau'},
    {'label': '(UTC-01:00) Atlantic/Cape_Verde', 'value': 'Atlantic/Cape_Verde'},
    {'label': '(UTC+01:00) Africa/Niamey', 'value': 'Africa/Niamey'},
    {'label': '(UTC+03:30) Asia/Tehran', 'value': 'Asia/Tehran'},
    {'label': '(UTC-04:00) America/Curacao', 'value': 'America/Curacao'},
    {'label': '(UTC+01:00) Africa/Malabo', 'value': 'Africa/Malabo'},
    {'label': '(UTC-03:00) Antarctica/Rothera', 'value': 'Antarctica/Rothera'},
    {'label': '(UTC+06:00) Asia/Qostanay', 'value': 'Asia/Qostanay'},
    {'label': '(UTC+13:00) Pacific/Auckland', 'value': 'Pacific/Auckland'},
    {'label': '(UTC-03:00) America/Argentina/Mendoza', 'value': 'America/Argentina/Mendoza'},
    {'label': '(UTC+03:00) Asia/Beirut', 'value': 'Asia/Beirut'},
    {'label': '(UTC-06:00) America/Regina', 'value': 'America/Regina'},
    {'label': '(UTC+01:00) Europe/Lisbon', 'value': 'Europe/Lisbon'},
    {'label': '(UTC+02:00) Europe/Vienna', 'value': 'Europe/Vienna'},
    {'label': '(UTC+00:00) Africa/Abidjan', 'value': 'Africa/Abidjan'},
    {'label': '(UTC-06:00) America/Managua', 'value': 'America/Managua'},
    {'label': '(UTC-04:00) America/Blanc-Sablon', 'value': 'America/Blanc-Sablon'},
    {'label': '(UTC-03:00) America/Argentina/Tucuman', 'value': 'America/Argentina/Tucuman'},
    {'label': '(UTC+10:30) Australia/Broken_Hill', 'value': 'Australia/Broken_Hill'},
    {'label': '(UTC+12:00) Pacific/Wallis', 'value': 'Pacific/Wallis'},
    {'label': '(UTC+05:00) Indian/Maldives', 'value': 'Indian/Maldives'},
    {'label': '(UTC+00:00) Africa/Accra', 'value': 'Africa/Accra'},
    {'label': '(UTC-08:00) America/Yakutat', 'value': 'America/Yakutat'},
    {'label': '(UTC+02:00) Africa/Maseru', 'value': 'Africa/Maseru'},
    {'label': '(UTC+07:00) Asia/Barnaul', 'value': 'Asia/Barnaul'},
    {'label': '(UTC+02:00) Europe/Warsaw', 'value': 'Europe/Warsaw'},
    {'label': '(UTC+02:00) Africa/Juba', 'value': 'Africa/Juba'},
    {'label': '(UTC+07:00) Asia/Novokuznetsk', 'value': 'Asia/Novokuznetsk'},
    {'label': '(UTC-08:00) America/Anchorage', 'value': 'America/Anchorage'},
    {'label': '(UTC-04:00) America/Kentucky/Louisville', 'value': 'America/Kentucky/Louisville'},
    {'label': '(UTC+07:00) Asia/Tomsk', 'value': 'Asia/Tomsk'},
    {'label': '(UTC+02:00) Europe/Skopje', 'value': 'Europe/Skopje'},
    {'label': '(UTC+02:00) Europe/Vatican', 'value': 'Europe/Vatican'},
    {'label': '(UTC+01:00) Africa/Porto-Novo', 'value': 'Africa/Porto-Novo'},
    {'label': '(UTC+12:00) Pacific/Majuro', 'value': 'Pacific/Majuro'},
    {'label': '(UTC-03:00) America/Belem', 'value': 'America/Belem'},
    {'label': '(UTC-07:00) Canada/Pacific', 'value': 'Canada/Pacific'},
    {'label': '(UTC+09:00) Asia/Khandyga', 'value': 'Asia/Khandyga'},
    {'label': '(UTC+01:00) Europe/Jersey', 'value': 'Europe/Jersey'},
    {'label': '(UTC-06:00) America/Inuvik', 'value': 'America/Inuvik'},
    {'label': '(UTC+09:00) Asia/Seoul', 'value': 'Asia/Seoul'},
    {'label': '(UTC+08:00) Asia/Shanghai', 'value': 'Asia/Shanghai'},
    {'label': '(UTC+07:00) Asia/Vientiane', 'value': 'Asia/Vientiane'},
    {'label': '(UTC-02:00) America/Noronha', 'value': 'America/Noronha'},
    {'label': '(UTC+00:00) Africa/Freetown', 'value': 'Africa/Freetown'},
    {'label': '(UTC+04:00) Asia/Tbilisi', 'value': 'Asia/Tbilisi'},
    {'label': '(UTC-06:00) America/Swift_Current', 'value': 'America/Swift_Current'},
    {'label': '(UTC+02:00) Europe/Gibraltar', 'value': 'Europe/Gibraltar'},
    {'label': '(UTC+04:00) Indian/Mauritius', 'value': 'Indian/Mauritius'},
    {'label': '(UTC+08:00) Asia/Taipei', 'value': 'Asia/Taipei'},
    {'label': '(UTC+01:00) Africa/Bangui', 'value': 'Africa/Bangui'},
    {'label': '(UTC+03:00) Europe/Minsk', 'value': 'Europe/Minsk'},
    {'label': '(UTC-04:00) America/Guyana', 'value': 'America/Guyana'},
    {'label': '(UTC-07:00) America/Fort_Nelson', 'value': 'America/Fort_Nelson'},
    {'label': '(UTC+08:00) Asia/Kuala_Lumpur', 'value': 'Asia/Kuala_Lumpur'},
    {'label': '(UTC-07:00) US/Arizona', 'value': 'US/Arizona'},
    {'label': '(UTC+03:00) Africa/Asmara', 'value': 'Africa/Asmara'},
    {'label': '(UTC+01:00) Atlantic/Madeira', 'value': 'Atlantic/Madeira'},
    {'label': '(UTC+05:00) Asia/Samarkand', 'value': 'Asia/Samarkand'},
    {'label': '(UTC+02:00) Europe/Ljubljana', 'value': 'Europe/Ljubljana'},
    {'label': '(UTC-04:00) America/Grand_Turk', 'value': 'America/Grand_Turk'},
    {'label': '(UTC-04:00) America/Puerto_Rico', 'value': 'America/Puerto_Rico'},
    {'label': '(UTC+03:00) Europe/Riga', 'value': 'Europe/Riga'},
    {'label': '(UTC+13:00) Pacific/Fakaofo', 'value': 'Pacific/Fakaofo'},
    {'label': '(UTC-05:00) America/North_Dakota/New_Salem', 'value': 'America/North_Dakota/New_Salem'},
    {'label': '(UTC+05:30) Asia/Kolkata', 'value': 'Asia/Kolkata'},
    {'label': '(UTC+03:00) Europe/Istanbul', 'value': 'Europe/Istanbul'},
    {'label': '(UTC+08:00) Asia/Singapore', 'value': 'Asia/Singapore'},
    {'label': '(UTC+12:00) Asia/Anadyr', 'value': 'Asia/Anadyr'},
    {'label': '(UTC+03:00) Asia/Jerusalem', 'value': 'Asia/Jerusalem'},
    {'label': '(UTC+09:00) Pacific/Palau', 'value': 'Pacific/Palau'},
    {'label': '(UTC+03:00) Asia/Kuwait', 'value': 'Asia/Kuwait'},
    {'label': '(UTC-04:00) America/Cuiaba', 'value': 'America/Cuiaba'},
    {'label': '(UTC-04:00) America/Grenada', 'value': 'America/Grenada'},
    {'label': '(UTC-06:00) America/Edmonton', 'value': 'America/Edmonton'},
    {'label': '(UTC-04:00) America/Campo_Grande', 'value': 'America/Campo_Grande'},
    {'label': '(UTC-07:00) America/Dawson', 'value': 'America/Dawson'},
    {'label': '(UTC+03:00) Indian/Mayotte', 'value': 'Indian/Mayotte'},
    {'label': '(UTC+03:00) Asia/Qatar', 'value': 'Asia/Qatar'},
    {'label': '(UTC-10:00) US/Hawaii', 'value': 'US/Hawaii'},
    {'label': '(UTC+03:00) Asia/Famagusta', 'value': 'Asia/Famagusta'},
    {'label': '(UTC+02:00) Europe/Rome', 'value': 'Europe/Rome'},
    {'label': '(UTC+09:00) Asia/Yakutsk', 'value': 'Asia/Yakutsk'},
    {'label': '(UTC-03:00) America/Maceio', 'value': 'America/Maceio'},
    {'label': '(UTC+07:00) Indian/Christmas', 'value': 'Indian/Christmas'},
    {'label': '(UTC-04:00) America/Iqaluit', 'value': 'America/Iqaluit'},
    {'label': '(UTC-06:00) US/Mountain', 'value': 'US/Mountain'},
    {'label': '(UTC+05:00) Asia/Dushanbe', 'value': 'Asia/Dushanbe'},
    {'label': '(UTC+08:00) Asia/Ulaanbaatar', 'value': 'Asia/Ulaanbaatar'},
    {'label': '(UTC-03:00) America/Argentina/Ushuaia', 'value': 'America/Argentina/Ushuaia'},
    {'label': '(UTC+02:00) Europe/Zagreb', 'value': 'Europe/Zagreb'},
    {'label': '(UTC+03:00) Antarctica/Syowa', 'value': 'Antarctica/Syowa'},
    {'label': '(UTC+00:00) Africa/Lome', 'value': 'Africa/Lome'},
    {'label': '(UTC-10:00) Pacific/Rarotonga', 'value': 'Pacific/Rarotonga'},
    {'label': '(UTC+02:00) Europe/Stockholm', 'value': 'Europe/Stockholm'},
    {'label': '(UTC+06:00) Asia/Almaty', 'value': 'Asia/Almaty'},
    {'label': '(UTC+02:00) Africa/Ceuta', 'value': 'Africa/Ceuta'},
    {'label': '(UTC+03:00) Africa/Kampala', 'value': 'Africa/Kampala'},
    {'label': '(UTC-07:00) America/Los_Angeles', 'value': 'America/Los_Angeles'},
    {'label': '(UTC-05:00) Pacific/Easter', 'value': 'Pacific/Easter'},
    {'label': '(UTC-04:00) America/Antigua', 'value': 'America/Antigua'},
    {'label': '(UTC+04:00) Indian/Mahe', 'value': 'Indian/Mahe'},
    {'label': '(UTC+10:00) Asia/Vladivostok', 'value': 'Asia/Vladivostok'},
    {'label': '(UTC-04:00) America/Toronto', 'value': 'America/Toronto'},
    {'label': '(UTC+09:30) Australia/Darwin', 'value': 'Australia/Darwin'},
    {'label': '(UTC-03:00) America/Santiago', 'value': 'America/Santiago'},
    {'label': '(UTC-03:00) America/Montevideo', 'value': 'America/Montevideo'},
    {'label': '(UTC+05:00) Asia/Aqtobe', 'value': 'Asia/Aqtobe'},
    {'label': '(UTC+02:00) Europe/Budapest', 'value': 'Europe/Budapest'},
    {'label': '(UTC+02:00) Europe/Madrid', 'value': 'Europe/Madrid'},
    {'label': '(UTC-04:00) Canada/Eastern', 'value': 'Canada/Eastern'},
    {'label': '(UTC-04:00) America/Lower_Princes', 'value': 'America/Lower_Princes'},
    {'label': '(UTC+07:00) Asia/Phnom_Penh', 'value': 'Asia/Phnom_Penh'},
    {'label': '(UTC-06:00) Pacific/Galapagos', 'value': 'Pacific/Galapagos'},
    {'label': '(UTC-03:00) America/Argentina/San_Juan', 'value': 'America/Argentina/San_Juan'},
    {'label': '(UTC-10:00) Pacific/Tahiti', 'value': 'Pacific/Tahiti'},
    {'label': '(UTC+02:00) Antarctica/Troll', 'value': 'Antarctica/Troll'},
    {'label': '(UTC+09:00) Asia/Tokyo', 'value': 'Asia/Tokyo'},
    {'label': '(UTC-07:00) US/Pacific', 'value': 'US/Pacific'},
    {'label': '(UTC-05:00) US/Central', 'value': 'US/Central'},
    {'label': '(UTC+05:00) Asia/Yekaterinburg', 'value': 'Asia/Yekaterinburg'},
    {'label': '(UTC+03:00) Asia/Aden', 'value': 'Asia/Aden'},
    {'label': '(UTC+02:00) Europe/Busingen', 'value': 'Europe/Busingen'},
    {'label': '(UTC+13:00) Pacific/Tongatapu', 'value': 'Pacific/Tongatapu'},
    {'label': '(UTC+02:00) Africa/Maputo', 'value': 'Africa/Maputo'},
    {'label': '(UTC+02:00) Europe/Bratislava', 'value': 'Europe/Bratislava'},
    {'label': '(UTC-04:00) America/Porto_Velho', 'value': 'America/Porto_Velho'},
    {'label': '(UTC-04:00) America/Detroit', 'value': 'America/Detroit'},
    {'label': '(UTC+02:00) Europe/Sarajevo', 'value': 'Europe/Sarajevo'},
    {'label': '(UTC+03:00) Africa/Addis_Ababa', 'value': 'Africa/Addis_Ababa'},
    {'label': '(UTC-05:00) America/North_Dakota/Beulah', 'value': 'America/North_Dakota/Beulah'},
    {'label': '(UTC+11:00) Pacific/Kosrae', 'value': 'Pacific/Kosrae'},
    {'label': '(UTC-02:00) America/Miquelon', 'value': 'America/Miquelon'},
    {'label': '(UTC+09:00) Asia/Jayapura', 'value': 'Asia/Jayapura'},
    {'label': '(UTC-05:00) America/Rankin_Inlet', 'value': 'America/Rankin_Inlet'},
    {'label': '(UTC-06:00) America/Bahia_Banderas', 'value': 'America/Bahia_Banderas'},
    {'label': '(UTC+12:00) Pacific/Norfolk', 'value': 'Pacific/Norfolk'},
    {'label': '(UTC-04:00) America/St_Barthelemy', 'value': 'America/St_Barthelemy'},
    {'label': '(UTC+02:00) Arctic/Longyearbyen', 'value': 'Arctic/Longyearbyen'},
    {'label': '(UTC-05:00) America/Winnipeg', 'value': 'America/Winnipeg'},
    {'label': '(UTC-08:00) America/Sitka', 'value': 'America/Sitka'},
    {'label': '(UTC-03:00) America/Thule', 'value': 'America/Thule'},
    {'label': '(UTC-07:00) America/Whitehorse', 'value': 'America/Whitehorse'},
    {'label': '(UTC+02:00) Africa/Lubumbashi', 'value': 'Africa/Lubumbashi'},
    {'label': '(UTC-04:00) America/St_Vincent', 'value': 'America/St_Vincent'},
    {'label': '(UTC+05:00) Asia/Qyzylorda', 'value': 'Asia/Qyzylorda'},
    {'label': '(UTC+03:00) Asia/Amman', 'value': 'Asia/Amman'},
    {'label': '(UTC+10:00) Antarctica/DumontDUrville', 'value': 'Antarctica/DumontDUrville'},
    {'label': '(UTC+02:00) Europe/Zurich', 'value': 'Europe/Zurich'},
    {'label': '(UTC+11:00) Australia/Sydney', 'value': 'Australia/Sydney'},
    {'label': '(UTC+07:00) Antarctica/Davis', 'value': 'Antarctica/Davis'},
    {'label': '(UTC-03:00) America/Santarem', 'value': 'America/Santarem'},
    {'label': '(UTC-09:30) Pacific/Marquesas', 'value': 'Pacific/Marquesas'},
    {'label': '(UTC-06:00) America/Cambridge_Bay', 'value': 'America/Cambridge_Bay'},
    {'label': '(UTC+11:00) Australia/Hobart', 'value': 'Australia/Hobart'},
    {'label': '(UTC+06:00) Asia/Bishkek', 'value': 'Asia/Bishkek'},
    {'label': '(UTC+02:00) Europe/San_Marino', 'value': 'Europe/San_Marino'},
    {'label': '(UTC+03:00) Europe/Volgograd', 'value': 'Europe/Volgograd'},
    {'label': '(UTC+00:00) Atlantic/Azores', 'value': 'Atlantic/Azores'},
    {'label': '(UTC+06:00) Indian/Chagos', 'value': 'Indian/Chagos'},
    {'label': '(UTC+07:00) Asia/Hovd', 'value': 'Asia/Hovd'},
    {'label': '(UTC+11:00) Pacific/Pohnpei', 'value': 'Pacific/Pohnpei'},
    {'label': '(UTC+09:00) Asia/Dili', 'value': 'Asia/Dili'},
    {'label': '(UTC+00:00) Africa/Nouakchott', 'value': 'Africa/Nouakchott'},
    {'label': '(UTC-07:00) America/Phoenix', 'value': 'America/Phoenix'},
    {'label': '(UTC+01:00) Atlantic/Canary', 'value': 'Atlantic/Canary'},
    {'label': '(UTC+00:00) Africa/Bamako', 'value': 'Africa/Bamako'},
    {'label': '(UTC-05:00) America/Guayaquil', 'value': 'America/Guayaquil'},
    {'label': '(UTC+10:00) Pacific/Saipan', 'value': 'Pacific/Saipan'},
    {'label': '(UTC+10:00) Pacific/Guam', 'value': 'Pacific/Guam'},
    {'label': '(UTC-06:00) Canada/Mountain', 'value': 'Canada/Mountain'},
    {'label': '(UTC-04:00) America/Indiana/Petersburg', 'value': 'America/Indiana/Petersburg'},
    {'label': '(UTC+06:00) Antarctica/Vostok', 'value': 'Antarctica/Vostok'},
    {'label': '(UTC+11:00) Pacific/Bougainville', 'value': 'Pacific/Bougainville'},
    {'label': '(UTC+02:00) Africa/Mbabane', 'value': 'Africa/Mbabane'},
    {'label': '(UTC-05:00) America/Panama', 'value': 'America/Panama'},
    {'label': '(UTC+11:00) Australia/Melbourne', 'value': 'Australia/Melbourne'},
    {'label': '(UTC+10:00) Australia/Brisbane', 'value': 'Australia/Brisbane'},
    {'label': '(UTC-04:00) America/Manaus', 'value': 'America/Manaus'},
    {'label': '(UTC+08:00) Asia/Manila', 'value': 'Asia/Manila'},
    {'label': '(UTC-02:30) America/St_Johns', 'value': 'America/St_Johns'},
    {'label': '(UTC-06:00) America/Guatemala', 'value': 'America/Guatemala'},
    {'label': '(UTC+07:00) Asia/Krasnoyarsk', 'value': 'Asia/Krasnoyarsk'},
    {'label': '(UTC-03:00) America/Argentina/Jujuy', 'value': 'America/Argentina/Jujuy'},
    {'label': '(UTC+02:00) Europe/Andorra', 'value': 'Europe/Andorra'},
    {'label': '(UTC+03:00) Indian/Antananarivo', 'value': 'Indian/Antananarivo'},
    {'label': '(UTC-03:00) America/Cayenne', 'value': 'America/Cayenne'},
    {'label': '(UTC+03:00) Asia/Bahrain', 'value': 'Asia/Bahrain'},
    {'label': '(UTC-05:00) America/Matamoros', 'value': 'America/Matamoros'},
    {'label': '(UTC+06:00) Asia/Dhaka', 'value': 'Asia/Dhaka'},
    {'label': '(UTC+02:00) Europe/Brussels', 'value': 'Europe/Brussels'},
    {'label': '(UTC+02:00) Africa/Bujumbura', 'value': 'Africa/Bujumbura'},
    {'label': '(UTC+03:00) Europe/Bucharest', 'value': 'Europe/Bucharest'},
    {'label': '(UTC+03:00) Europe/Chisinau', 'value': 'Europe/Chisinau'},
    {'label': '(UTC-05:00) America/Rio_Branco', 'value': 'America/Rio_Branco'},
    {'label': '(UTC-03:00) Atlantic/Stanley', 'value': 'Atlantic/Stanley'},
    {'label': '(UTC-07:00) America/Hermosillo', 'value': 'America/Hermosillo'},
    {'label': '(UTC-04:00) America/Anguilla', 'value': 'America/Anguilla'},
    {'label': '(UTC+01:00) Europe/London', 'value': 'Europe/London'},
    {'label': '(UTC+00:00) Africa/Sao_Tome', 'value': 'Africa/Sao_Tome'},
    {'label': '(UTC+14:00) Pacific/Kiritimati', 'value': 'Pacific/Kiritimati'},
    {'label': '(UTC-07:00) America/Tijuana', 'value': 'America/Tijuana'},
    {'label': '(UTC+02:00) Europe/Oslo', 'value': 'Europe/Oslo'},
    {'label': '(UTC-04:00) America/Indiana/Winamac', 'value': 'America/Indiana/Winamac'},
    {'label': '(UTC+07:00) Asia/Ho_Chi_Minh', 'value': 'Asia/Ho_Chi_Minh'},
    {'label': '(UTC-05:00) Canada/Central', 'value': 'Canada/Central'},
    {'label': '(UTC-06:00) America/Chihuahua', 'value': 'America/Chihuahua'},
    {'label': '(UTC-03:00) America/Argentina/Cordoba', 'value': 'America/Argentina/Cordoba'},
    {'label': '(UTC+00:00) America/Danmarkshavn', 'value': 'America/Danmarkshavn'},
    {'label': '(UTC-03:00) America/Goose_Bay', 'value': 'America/Goose_Bay'},
    {'label': '(UTC+11:00) Australia/Lord_Howe', 'value': 'Australia/Lord_Howe'},
    {'label': '(UTC+02:00) Africa/Khartoum', 'value': 'Africa/Khartoum'},
    {'label': '(UTC+01:00) Europe/Isle_of_Man', 'value': 'Europe/Isle_of_Man'},
    {'label': '(UTC-08:00) America/Metlakatla', 'value': 'America/Metlakatla'},
    {'label': '(UTC+02:00) Africa/Cairo', 'value': 'Africa/Cairo'},
    {'label': '(UTC-04:00) America/La_Paz', 'value': 'America/La_Paz'},
    {'label': '(UTC+07:00) Asia/Novosibirsk', 'value': 'Asia/Novosibirsk'},
    {'label': '(UTC+04:00) Asia/Baku', 'value': 'Asia/Baku'},
    {'label': '(UTC-11:00) Pacific/Pago_Pago', 'value': 'Pacific/Pago_Pago'},
    {'label': '(UTC+12:00) Pacific/Fiji', 'value': 'Pacific/Fiji'},
    {'label': '(UTC-03:00) America/Recife', 'value': 'America/Recife'},
    {'label': '(UTC+02:00) Europe/Luxembourg', 'value': 'Europe/Luxembourg'},
    {'label': '(UTC+08:00) Asia/Brunei', 'value': 'Asia/Brunei'},
    {'label': '(UTC+02:00) Europe/Paris', 'value': 'Europe/Paris'},
    {'label': '(UTC+04:00) Asia/Dubai', 'value': 'Asia/Dubai'},
    {'label': '(UTC-04:00) America/Guadeloupe', 'value': 'America/Guadeloupe'},
    {'label': '(UTC-04:00) America/Barbados', 'value': 'America/Barbados'},
    {'label': '(UTC+00:00) Atlantic/Reykjavik', 'value': 'Atlantic/Reykjavik'},
    {'label': '(UTC-04:00) America/New_York', 'value': 'America/New_York'},
    {'label': '(UTC+02:00) Africa/Lusaka', 'value': 'Africa/Lusaka'},
    {'label': '(UTC+01:00) Europe/Guernsey', 'value': 'Europe/Guernsey'},
    {'label': '(UTC+05:00) Asia/Karachi', 'value': 'Asia/Karachi'},
    {'label': '(UTC+02:00) Europe/Tirane', 'value': 'Europe/Tirane'},
    {'label': '(UTC+06:30) Asia/Yangon', 'value': 'Asia/Yangon'},
    {'label': '(UTC+02:00) Africa/Windhoek', 'value': 'Africa/Windhoek'},
    {'label': '(UTC-03:00) America/Argentina/Buenos_Aires', 'value': 'America/Argentina/Buenos_Aires'},
    {'label': '(UTC-04:00) America/Port_of_Spain', 'value': 'America/Port_of_Spain'},
    {'label': '(UTC-05:00) America/Indiana/Tell_City', 'value': 'America/Indiana/Tell_City'},
    {'label': '(UTC-04:00) America/Indiana/Indianapolis', 'value': 'America/Indiana/Indianapolis'},
    {'label': '(UTC-07:00) America/Vancouver', 'value': 'America/Vancouver'},
    {'label': '(UTC+11:00) Pacific/Efate', 'value': 'Pacific/Efate'},
    {'label': '(UTC+01:00) Africa/Libreville', 'value': 'Africa/Libreville'},
    {'label': '(UTC-03:00) America/Moncton', 'value': 'America/Moncton'},
    {'label': '(UTC+06:00) Asia/Urumqi', 'value': 'Asia/Urumqi'},
    {'label': '(UTC-06:00) America/Belize', 'value': 'America/Belize'},
    {'label': '(UTC+10:30) Australia/Adelaide', 'value': 'Australia/Adelaide'},
    {'label': '(UTC+03:00) Indian/Comoro', 'value': 'Indian/Comoro'},
    {'label': '(UTC+08:00) Asia/Makassar', 'value': 'Asia/Makassar'},
    {'label': '(UTC+02:00) Europe/Amsterdam', 'value': 'Europe/Amsterdam'},
    {'label': '(UTC+05:00) Asia/Aqtau', 'value': 'Asia/Aqtau'},
    {'label': '(UTC-03:00) America/Argentina/La_Rioja', 'value': 'America/Argentina/La_Rioja'},
    {'label': '(UTC+12:00) Asia/Kamchatka', 'value': 'Asia/Kamchatka'},
    {'label': '(UTC+03:00) Europe/Kyiv', 'value': 'Europe/Kyiv'},
    {'label': '(UTC+12:00) Pacific/Wake', 'value': 'Pacific/Wake'},
    {'label': '(UTC+10:00) Australia/Lindeman', 'value': 'Australia/Lindeman'},
    {'label': '(UTC+11:00) Asia/Srednekolymsk', 'value': 'Asia/Srednekolymsk'},
    {'label': '(UTC+00:00) Africa/Bissau', 'value': 'Africa/Bissau'},
    {'label': '(UTC+03:00) Europe/Helsinki', 'value': 'Europe/Helsinki'},
    {'label': '(UTC-04:00) America/Caracas', 'value': 'America/Caracas'},
    {'label': '(UTC+02:00) Europe/Berlin', 'value': 'Europe/Berlin'},
    {'label': '(UTC+12:00) Pacific/Tarawa', 'value': 'Pacific/Tarawa'},
    {'label': '(UTC-05:00) America/Atikokan', 'value': 'America/Atikokan'},
    {'label': '(UTC-04:00) America/Indiana/Vevay', 'value': 'America/Indiana/Vevay'},
    {'label': '(UTC+02:00) Europe/Podgorica', 'value': 'Europe/Podgorica'},
    {'label': '(UTC-06:00) America/Denver', 'value': 'America/Denver'},
    {'label': '(UTC-04:00) America/Havana', 'value': 'America/Havana'},
    {'label': '(UTC-06:00) America/Boise', 'value': 'America/Boise'},
    {'label': '(UTC-06:00) America/Costa_Rica', 'value': 'America/Costa_Rica'},
    {'label': '(UTC+00:00) America/Scoresbysund', 'value': 'America/Scoresbysund'},
    {'label': '(UTC+02:00) Europe/Belgrade', 'value': 'Europe/Belgrade'},
    {'label': '(UTC+12:00) Pacific/Funafuti', 'value': 'Pacific/Funafuti'},
    {'label': '(UTC-04:00) America/Nassau', 'value': 'America/Nassau'},
    {'label': '(UTC+01:00) Africa/Kinshasa', 'value': 'Africa/Kinshasa'},
    {'label': '(UTC-04:00) America/St_Kitts', 'value': 'America/St_Kitts'},
    {'label': '(UTC+03:00) Europe/Mariehamn', 'value': 'Europe/Mariehamn'},
    {'label': '(UTC+02:00) Africa/Gaborone', 'value': 'Africa/Gaborone'},
    {'label': '(UTC+11:00) Asia/Magadan', 'value': 'Asia/Magadan'},
    {'label': '(UTC+03:00) Europe/Simferopol', 'value': 'Europe/Simferopol'},
    {'label': '(UTC-05:00) America/Cancun', 'value': 'America/Cancun'},
    {'label': '(UTC+11:00) Asia/Sakhalin', 'value': 'Asia/Sakhalin'},
    {'label': '(UTC-03:00) America/Argentina/San_Luis', 'value': 'America/Argentina/San_Luis'},
    {'label': '(UTC+04:00) Indian/Reunion', 'value': 'Indian/Reunion'},
    {'label': '(UTC-05:00) America/Resolute', 'value': 'America/Resolute'},
    {'label': '(UTC-04:00) America/Santo_Domingo', 'value': 'America/Santo_Domingo'},
    {'label': '(UTC+11:00) Pacific/Noumea', 'value': 'Pacific/Noumea'},
    {'label': '(UTC+00:00) UTC', 'value': 'UTC'},
    {'label': '(UTC+01:00) Africa/Algiers', 'value': 'Africa/Algiers'},
    {'label': '(UTC-05:00) America/Chicago', 'value': 'America/Chicago'},
    {'label': '(UTC+02:00) Africa/Harare', 'value': 'Africa/Harare'},
    {'label': '(UTC-08:00) Pacific/Pitcairn', 'value': 'Pacific/Pitcairn'},
    {'label': '(UTC-05:00) America/Eirunepe', 'value': 'America/Eirunepe'},
    {'label': '(UTC+13:00) Antarctica/McMurdo', 'value': 'Antarctica/McMurdo'},
    {'label': '(UTC-03:00) America/Halifax', 'value': 'America/Halifax'},
    {'label': '(UTC-02:00) America/Nuuk', 'value': 'America/Nuuk'},
    {'label': '(UTC-04:00) America/Aruba', 'value': 'America/Aruba'},
    {'label': '(UTC-04:00) America/Port-au-Prince', 'value': 'America/Port-au-Prince'},
    {'label': '(UTC+05:00) Asia/Ashgabat', 'value': 'Asia/Ashgabat'},
    {'label': '(UTC+08:45) Australia/Eucla', 'value': 'Australia/Eucla'},
    {'label': '(UTC+04:00) Asia/Muscat', 'value': 'Asia/Muscat'},
    {'label': '(UTC+04:00) Asia/Yerevan', 'value': 'Asia/Yerevan'},
    {'label': '(UTC+05:00) Antarctica/Mawson', 'value': 'Antarctica/Mawson'},
    {'label': '(UTC+02:00) Europe/Monaco', 'value': 'Europe/Monaco'},
    {'label': '(UTC+04:30) Asia/Kabul', 'value': 'Asia/Kabul'},
    {'label': '(UTC-03:00) America/Argentina/Salta', 'value': 'America/Argentina/Salta'},
    {'label': '(UTC-06:00) America/Mexico_City', 'value': 'America/Mexico_City'},
    {'label': '(UTC+07:00) Asia/Bangkok', 'value': 'Asia/Bangkok'},
    {'label': '(UTC-04:00) America/Indiana/Vincennes', 'value': 'America/Indiana/Vincennes'},
    {'label': '(UTC-07:00) America/Dawson_Creek', 'value': 'America/Dawson_Creek'},
    {'label': '(UTC+10:00) Asia/Ust-Nera', 'value': 'Asia/Ust-Nera'},
    {'label': '(UTC+01:00) Europe/Dublin', 'value': 'Europe/Dublin'},
    {'label': '(UTC+03:00) Africa/Dar_es_Salaam', 'value': 'Africa/Dar_es_Salaam'},
    {'label': '(UTC+07:00) Asia/Pontianak', 'value': 'Asia/Pontianak'},
    {'label': '(UTC+11:00) Antarctica/Macquarie', 'value': 'Antarctica/Macquarie'},
    {'label': '(UTC+03:00) Europe/Athens', 'value': 'Europe/Athens'},
    {'label': '(UTC-04:00) America/Montserrat', 'value': 'America/Montserrat'},
    {'label': '(UTC-05:00) America/Bogota', 'value': 'America/Bogota'},
    {'label': '(UTC+01:00) Africa/Casablanca', 'value': 'Africa/Casablanca'},
    {'label': '(UTC+03:00) Asia/Baghdad', 'value': 'Asia/Baghdad'},
    {'label': '(UTC+02:00) Africa/Blantyre', 'value': 'Africa/Blantyre'},
    {'label': '(UTC+02:00) Europe/Prague', 'value': 'Europe/Prague'},
    {'label': '(UTC-09:00) Pacific/Gambier', 'value': 'Pacific/Gambier'},
    {'label': '(UTC+00:00) Atlantic/St_Helena', 'value': 'Atlantic/St_Helena'},
    {'label': '(UTC+03:00) Asia/Riyadh', 'value': 'Asia/Riyadh'},
    {'label': '(UTC+08:00) Australia/Perth', 'value': 'Australia/Perth'},
    {'label': '(UTC-06:00) America/Monterrey', 'value': 'America/Monterrey'},
    {'label': '(UTC-06:00) America/Ciudad_Juarez', 'value': 'America/Ciudad_Juarez'},
    {'label': '(UTC+06:00) Asia/Thimphu', 'value': 'Asia/Thimphu'},
    {'label': '(UTC-03:00) America/Bahia', 'value': 'America/Bahia'},
    {'label': '(UTC+01:00) Africa/El_Aaiun', 'value': 'Africa/El_Aaiun'},
    {'label': '(UTC+01:00) Africa/Lagos', 'value': 'Africa/Lagos'},
    {'label': '(UTC+04:00) Europe/Saratov', 'value': 'Europe/Saratov'},
    {'label': '(UTC+02:00) Europe/Vaduz', 'value': 'Europe/Vaduz'},
    {'label': '(UTC-05:00) America/Jamaica', 'value': 'America/Jamaica'},
    {'label': '(UTC+05:00) Asia/Atyrau', 'value': 'Asia/Atyrau'},
    {'label': '(UTC-11:00) Pacific/Midway', 'value': 'Pacific/Midway'},
    {'label': '(UTC+02:00) Asia/Gaza', 'value': 'Asia/Gaza'},
    {'label': '(UTC+03:00) Africa/Nairobi', 'value': 'Africa/Nairobi'},
    {'label': '(UTC-07:00) America/Mazatlan', 'value': 'America/Mazatlan'},
    {'label': '(UTC+03:00) Europe/Tallinn', 'value': 'Europe/Tallinn'},
    {'label': '(UTC-06:00) America/El_Salvador', 'value': 'America/El_Salvador'}
)

CONFERENCE_PROPERTIES = (
    "uid",
    "timezone",
    "dtstart",
    "dtend",
    "summary",
    "created",
    "last_modified",
    "description",
    "url_event",
    "categories",
    "x_telemost_conference",
    "organizer",
    "attendee",
    "location",
    "recurrence_id",
)

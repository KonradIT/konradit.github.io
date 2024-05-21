import sys, json
from jinja2 import Template
from datetime import datetime, timedelta

json_file = sys.argv[1] + "/resume.json"
template_text = """
<html>
	<head>
		<title>Konrad Iturbe's Resume</title>
		<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
		<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
		<link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
		<link rel="manifest" href="../site.webmanifest">
		<link rel="mask-icon" href="../safari-pinned-tab.svg" color="#5bbad5">
		<meta name="msapplication-TileColor" content="#da532c">
		<meta name="theme-color" content="#ffffff">
		<style>
			body {
				font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
			}

			@media only screen and (min-width: 1000px) {
				body {
					padding-left: 20%;
					padding-right: 20%;
				}
			}

			@media print {
				.noPrint {
					display:none;
				}
			}
			@media screen {
				.onlyPrint {
					display: none;
				}
			}
			#experience-nugget {
					padding-left: 5px;
					padding-right: 5px;
					border-radius: 5px;
					border-color: black;
					border-style: solid;
					border-width: thin;
					display: inline-block;
					color: black;
			}
			a:link {
				color: blue
			}

			a:active {
				color: blue
			}

			a:visited {
				color: blue
			}

			a:hover {
				color: blue
			}
			#workxp {
				line-height: 1.3;
			}
		</style>
		<meta name="viewport" content="width=device-width" />
	</head>

	<body>
		<table>
			<tr>
				<td>
					<b id="header-text">{{ data.get("details").get("name")[0] }} {{ data.get("details").get("name")[1] }}</b><br />{{ data.get("details").get("dob") }} - {{ data.get("details").get("location") }} <br />
					<a
						href="{{ data.get("details").get("twitter")}}"
						target="_top"
						>Twitter</a
					>
					|
					<a href="{{ data.get("details").get("github")}}" target="_top">GitHub</a
					><br><i>{{ data.get("details").get("email")}}</i><br />
     				<br class="noPrint"><a href="https://konraditurbe.dev/resume/resume.json" target="_top" class="noPrint">View resume
                        as JSON</a><br><a class="noPrint" href="https://konraditurbe.dev/resume/resume.pdf" target="_top">View resume as PDF</a>
                <a class="onlyPrint" href="https://konraditurbe.dev/resume/" target="_top">View
                        resume as HTML website</a>
				</td>
			</tr>

			<tr id="main">
				<td>
					<b id="cell-text">Main:</b><br />
					<ul>
						{% for item in data.get("tidbits") %}
							<li class="{{"noPrint" if loop.index0 not in data.get("tidbits_for_pdf") else "" }}">{{ item }}</li>
						{% endfor %}
					</ul>
				</td>
			</tr>
		</table>

		<div id="skills">
			<br /><b id="cell-text">Skills:</b>
			<ul>
				{% for item in data.get("skills") %}
					<li>{{ item.get("name") }}   -    <i>({{ item.get("proficiency") }})</i></li>
				{% endfor %}
			</ul>
			<br class="noPrint" /><b class="noPrint" id="cell-text">Education: </b>
			<ul>
				<li class="noPrint">{{ data.get("education")[0][1] }} - {{ data.get("education")[0][0] }}</li>
			</ul>
			<br /><b id="cell-text">Certificates: </b>
			<ul>
				{% for item in data.get("certificates") %}
					<li>{{ item }}</li>
				{% endfor %}
			</ul>
		</div>

		<div id="workxp">
			<b id="cell-text">Work experience: </b>
			<ul>
				{% for item in data.get("work_experience")|reverse %}
					<li><b>{{ item.get("company") }} // {{ item.get("start_date") }} {{ "- " ~ item.get("end_date") if item.get("end_date") != None else " - present day" }}</b> ... <i>[{{ item.get("type") }}]</i> {% for expitem in item.get("skills_used") %} <div id="experience-nugget">{{ expitem }}</div>{% endfor %} <br>{{ item.get("tasks") }}</li><br>
				{% endfor %}
			</ul>
		</div>
	</body>
</html>
"""
with open(json_file) as json_binary_reader:
	resume_content = json_binary_reader.read()
	try:
		resume_json = json.loads(resume_content)
	except:
		sys.exit(1)
	template = Template(template_text)
	humanreadable = "%m/%Y"

	for index, item in enumerate(resume_json.get("work_experience")):
		root = resume_json["work_experience"][index]
		start = datetime.fromtimestamp(item.get("start_date"))
		if "end_date" in item and item.get("end_date") != None:
			end = datetime.fromtimestamp(item.get("end_date"))
			root["end_date"] = end.strftime(humanreadable)
		root["start_date"] = start.strftime(humanreadable)

	print(template.render(data=resume_json))
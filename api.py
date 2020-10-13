from setting import *

app = Flask(__name__)
CORS(app)

openport = os.environ['PORT']

def convertToNum(value):
	value = value.replace(",","")
	return int(value)

def getVacancyDetail(url, options):
	driver = webdriver.Chrome(chrome_options=options)
	
	print(url)
	driver.get(url)

	job = {}

	comName = ""
	comPicture = ""
	comLocation = ""
	jobTitle = ""
	yearExperience = ""
	experiencePosition = ""

	try:
		driver.find_element_by_xpath(".//div[@class='content-error text-center']")
		print("Tidak Error")
		return job
	except:
		pass

	error  = 0
	while(error < 10):
		try:
			driver.find_element_by_tag_name('body').send_keys(
						Keys.END)  # Scroll to Buttom of the page

			# Get Job Information
			jobTitle = driver.find_element_by_xpath(".//h1[@id='position_title']").text
			experience = driver.find_element_by_xpath(".//p[@id='years_of_experience']//span[@id='years_of_experience']").text
			yearExperience = experience.split(" ")[1]
			experiencePosition = experience.replace("Min {year} tahun ".format(year=yearExperience), "")

			# Get Company Information
			comName = driver.find_element_by_xpath(".//div[@id='company_name']").text
			try:
				comLocation = driver.find_element_by_xpath(".//div[@id='location']//span[@id='single_work_location']").text
			except:
				pass
			try:
				comPicture = driver.find_element_by_xpath(".//div[@class='logo_sm_wrap']/img[@id='company_logo']").get_attribute("src")
			except:
				pass

			job = {
				"jobTitle": jobTitle,
				"experience": {
					"years": int(yearExperience),
					"position": experiencePosition
				},
				"company":{
					"name": comName,
					"picture": comPicture,
					"location": comLocation
				}
			}

			error = 11
		except Exception as e:
			error += 1
			print("Error Getting Detail --- Try -", error)
			print(e)

			driver.execute_script('window.localStorage.clear();')
			driver.close()
			driver.quit()

			driver = webdriver.Chrome(chrome_options=options)
			driver.get(url)
			time.sleep(3)

			driver.find_element_by_tag_name('body').send_keys(
					Keys.END)  # Scroll to Buttom of the page

	driver.execute_script('window.localStorage.clear();')
	driver.close()
	driver.quit()

	return job

def getJobVacancy(url, start, end):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-impl-side-painting')
	chrome_options.add_argument('--disable-gpu-sandbox')
	chrome_options.add_argument('--disable-accelerated-2d-canvas')
	chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
	chrome_options.add_argument('--test-type=ui')
	chrome_options.add_argument('--disable-dev-shm-usage')  # fixing crash tab
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument(
		'--allow-running-insecure-content')  # Enable java script
	chrome_options.add_argument('--window-size=1280x1696')
	chrome_options.add_argument(
		'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0')

	driver = webdriver.Chrome(chrome_options=chrome_options)

	print(url)
	driver.get(url)

	jobs = []

	try:
		condition = True
		while(condition):
			try:
				driver.find_element_by_tag_name('body').send_keys(
					Keys.END)  # Scroll to Buttom of the page
				WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.XPATH, 
					".//div[@id='job_listing_panel']"))
				)
				condition = False
			except:
				print("Error - Cannot Get Listing")
				driver.execute_script('window.localStorage.clear();')
				driver.close()
				driver.quit()

				driver = webdriver.Chrome(chrome_options=chrome_options)
				driver.get(url)

		jobLinks = driver.find_elements_by_xpath(".//div[@class='position-title header-text']/a")

		i = 0
		length = len(jobLinks)
		while(i < length):
			link = jobLinks[i]

			driver.find_element_by_tag_name('body').send_keys(
                Keys.END)  # Scroll to Buttom of the page
			length = len(jobLinks)

			job = getVacancyDetail(link.get_attribute("href"), chrome_options)

			if(job):
				jobs.append(job)

			jobLinks = driver.find_elements_by_xpath(".//div[@class='position-title header-text']/a")
			i += 1
		
	except Exception as ex:
		print("ERROR-GETTING-DATA :")
		print(ex)

	print(jobs)
	
	driver.execute_script('window.localStorage.clear();')
	driver.close()
	driver.quit()

	return jobs

@app.route('/job', methods=['GET'])
def mainRMQ():	
	start = int(request.args["start"]) if 'start' in request.args else 1
	end = int(request.args["end"]) if 'end' in request.args else 1

	url = "https://www.jobstreet.co.id/id/job-search/job-vacancy.php"
	inner = getJobVacancy(url, start, end)

	return json.dumps(inner)



# if __name__ == '__main__':
# 	try:
# 		mainRMQ()
# 	except KeyboardInterrupt:
# 		print('Interrupted')
# 		try:
# 			sys.exit(0)
# 		except SystemExit:
# 			os._exit(0)

if __name__ == '__main__':
	# test()
	app.run(host='0.0.0.0', port=openport, debug=False, threaded=True)

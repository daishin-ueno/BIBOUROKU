from serpapi import GoogleSearch
import re
import pandas as pd
import platform
import os
import sys

def make_folder () :

    if platform.system() == 'Windows':
        path_sep = "\\"
    else:
        path_sep = "/"
    #-----------------------------------
    #print(raw_data_site_num)
    result_pass= os.path.abspath(os.path.dirname(__file__))+ path_sep+ "Results"
    if not os.path.isdir(result_pass) :
        os.mkdir(result_pass)
    folder_path = os.path.abspath(os.path.dirname(__file__))+ path_sep+ "Results"+ path_sep+\
                                                           os.path.splitext(os.path.basename(sys.argv[0]))[0]+"_result"
    i = 0
    if os.path.isdir(folder_path) :
        while os.path.exists(folder_path+"_"+str(i)) :
            i = i+1
            
        folder_path=folder_path+"_"+str(i)
        os.mkdir(folder_path)

    else :
        os.mkdir(folder_path)
    return (folder_path+path_sep)

#start define start page 
params = {
  "engine": "google_scholar",
  "q": "biology",
  "api_key": "273aa874064ffe3dcb5872dd735444a600959757f9df2d8174705c3adfec7488",
  #"scisbd" :1,
	}

search = GoogleSearch(params)
results = search.get_dict()

for result in results:
	print(result)

#resultsの中身
#search_metadata
#search_parameters
#search_information
#organic_results
#related_searches
#pagination
#serpapi_pagination



print(results["search_information"])
#results["search_information"]の中身
#{'organic_results_state': 'Results for exact spelling', 'total_results': 6160000, 'time_taken_displayed': 0.03, 'query_displayed': 'biology'}

total_num = results["search_information"]['total_results']
print(total_num)

#test_num_list = [10,20,30,40,50,60,70,80,90,100]
test_num_list = [10]
for test_num in test_num_list:
	params = {
  "engine": "google_scholar",
  "q": "biology",
  "api_key": "273aa874064ffe3dcb5872dd735444a600959757f9df2d8174705c3adfec7488",
  "start" : test_num,
  "as_rr":1, #reviewerを入れるかどうか 1 removing
  "as_sdt":0 #patentを入れるか入れないか
  #"scisbd" :1,
	}
	organic_results = results["organic_results"]
	print("############  organic_results   ###############")


	sum_list = []
	for organic_result in organic_results:
		#print(organic_result)
		publication_info = organic_result["publication_info"]["summary"]
		if "book" in publication_info:
			continue

		year = re.sub( '[^0-9]', '', publication_info)

		cite_inform = organic_result["inline_links"]
		cite_num = cite_inform["cited_by"]["total"]

		sum_list.append([organic_result['title'],year,cite_num,organic_result['link']])

	table = pd.DataFrame(sum_list,columns=["Tite","Year","Cite_num","Link"])
	folder_path = make_folder ()
	table.to_csv(folder_path+"output.csv",index = False)




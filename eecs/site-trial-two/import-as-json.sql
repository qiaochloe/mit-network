-- MIT eecs data 

SELECT
	CONCAT("[",
		GROUP_CONCAT(
			CONCAT('{\"course_title\":\"',course_title,'\",'),
			CONCAT('\"course_code\":\"',course_code,'\"}')
		)
	,"]")
AS json FROM eecs

-- MIT prereqs data

SELECT
	CONCAT("[",
		GROUP_CONCAT(
			CONCAT('{\"source\":\"',course,'\",'),
			CONCAT('\"target\":\"',prereq,'\"}')
		)
	,"]")
AS json FROM prerequisites

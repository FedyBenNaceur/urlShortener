# urlShortener

<div> A basic URL shortener implemented using redis and python,  
  it allows a user to shorten an and save it. </div>
  
<div>When an user gives a URL in standard format, in addition to their e-mail as an authentication
token, the system should return a shortened URL, by:
  <li>checking if a short version for the same URL already exists.</li>
    <li>if the short version does not exist, it should generate and record the link between the long
      URL and the short one.</li>
      When an user gives a short URL, the system should return the long version if it exists, and an
error if it is not the case.
The system records statistics:
  <li> how many URLs have been inserted per user.</li>
  <li> how many requests were made for each short URL.</li>
  When you execute the script you'll be asked to enter your email and a url to shorten.
  You can specify options to view statistics with the following flags : 
  <li> -s to show how many users and urls are stored in the data base.</li>
    <li> -us to show user stats</li>
      <li> -qs to show stats about a specific query</li>
        <li>-lu to list all the users of the data base</li>
  

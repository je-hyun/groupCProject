* ID:003 , Use-case: Location Input as Address
    * Description: In the preferences pages, the location can be input as a regular string address. The address is converted to coordinates and saved in the database. (Bonus: also, I made the map display and pull latitude/longitude from the database)
    * Actor: Regular User
    * Assigned to : Je Hyun Kim
    * Location in project: /app/location_utils/addressToCoordinates.py, /app/location_utils/coordinatesToAddress.py, app/models.py (Event.get_address()), app/main/routes.py ()
    * Refs: use-case_doc, issue (http://link_to_github_issue_item)
    * Completion status: Finished.
    * Issues/Difficulties: None.
* ID:004 , Use-case: Formating the events page
    * Description: Adding a style sheet to the events page to make it look          
       nice
    * Actor: Front end
    * Assigned to : George Stephanoff
    * Location in project:/app/static/css/events_page.css,      
       app/templates/events_page.html
    * Refs: use-case_doc, issue (http://link_to_github_issue_item)
    * Completion status: Finished.
    * Issues/Difficulties: None.
* ID: 005, Use Case:  Create Page for individual events. Add more dummy data for database
    * Description: creating a page for when an individual even is selected on calendar.
    * Actor: Regular User
    * Assigned to: Christopher Fitzpatrick
    * Location In project: \app\models & \app\templates\calender
    * Refs: use-case_doc, issue (http://link_to_github_issue_item)
    * Completion Status: Finished
    * Issues/difficulties: None
* ID:006 , Use-case: Sorting Events Page
    * Description: Has a drop down menu that will give you options to sort events by name, cost, day 
    * Actor: Regular User
    * Assigned to : Matthew Nguyen
    * Location in project: /app/static/css/events_page.css, /app/main/routes.py, /app/templates/events_page.html, /app/templates/layout.html
    * Refs: use-case_doc, issue (http://link_to_github_issue_item)
    * Completion status: Finished.
    * Issues/Difficulties: None.
*ID:007 , Use-case: Make a work time form and save work time data to the database
      * Description: create a work form html file to input timeslot when you are unavailable. The work time data is stored in the database and will filter available events based on the time slots you entered
      * Actor: Regular User
      * Assigned to: Kamil Peza
      * Refs: Refs: use-case_doc, issue (http://link_to_github_issue_item)
      * Completion status: Just needs some fixing up
      * Issues/Difficulties: had trouble with display template because there are two 
      route.py files and had to specify which one to use 
* ID: 009, Use-case: Creating Events Page
    * Description: Display a list of events on the right side of the page (Querying from database)
    * Actor: Regular User
    * Assigned to: Andrew O'Leary
    * Location in project: /app/templates/events_page.html
    * Refs: use-case_doc, issue
(http://link_to_github_issue_item)
    * Completion Status: Finished.
    * Issues/Difficulties: None.
* ID:0010 , Use-case: Like_Event
    * Description: In the Event page, Add a like button which when clicked Adds to a likeEvent in DB. Also Add LikeEvent page which prints out the user id, name and event id and name
    * Assigned to : Nav
    * Location in project: /app/routes.py, app/main/routes.py, app/main/templates/layout.html,
app/main/templates/event_page.html, app/main/templates/like_page.html
    * Refs: use-case_doc, issue  (https://github.com/je-hyun/groupCProject/tree/like_page)
    * Completion status: Finished.
    * Issues/Difficulties:: currently on like_page(branch), waiting to merge, Code is functional

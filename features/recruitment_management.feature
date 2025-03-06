Feature: Recruitment Management in OrangeHRM
  As an HR manager,
  I want to manage job vacancies and candidate applications
  So that I can streamline the hiring process effectively

  Background:
    Given I am on the OrangeHRM login page
    When I enter valid credentials "Admin" and "admin123"
    And I click on the login button
    Then I should be redirected to the OrangeHRM dashboard
    And I navigate to the "Recruitment" tab

  # Scenario 1: Add a New Candidate
  Scenario: Add a new candidate for a job vacancy
    Given I click on the "Candidates" section
    When I click on the "Add" button
    And I enter the candidate's first name John
    And I enter the candidate's last name Doe
    And I enter the candidate's email john.doe@example.com
    And I select a job vacancy "Software Engineer"
    #And I upload the candidate's resume from "C:/Documents/Resume/JohnDoe.pdf"
    And I upload the candidate's resume from "~/Documents/Falguni/Cover_letter.pdf"
    And I click on the "Save" button
    #Then I should see a success message "Successfully Saved" - ( since the toaster msg dissapears fast m excluding this step
    Then I should see candidate's name John Doe displayed on the redirected page
##
  # Scenario 2: Search for a Candidate
  Scenario: Search for a candidate by name
    Given I am on the "Candidates" section
    When I enter the candidate's name John Doe in the search field
    And I click on the "Search" button
    Then I should see John Doe listed in the search results
#
#  # Scenario 3: Delete a Candidate from the List
  Scenario: Delete a candidate from the recruitment list
    When I select the candidate from the search results
    And I click on the "Delete" button
    And I confirm the deletion
    Then I should see the table updated without Candidate John Doe

#  # Scenario 4: Validate Empty Candidate Submission
  Scenario: Attempt to submit a candidate form without mandatory fields
    Given I click on the "Candidates" section
    When I click on the "Add" button
    And I click on the "Save" button without filling any fields
    Then I should see validation messages for required fields
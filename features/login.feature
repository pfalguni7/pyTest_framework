Feature: login
  @smoke
  Scenario Outline: User logs in with valid credentials
    Given the user is on the login page
    When the user enters valid "<username>" username and "<password>" password
    And clicks on the login button
    Then the user should be able to see the dashboard page

    Examples:
    | username | password |
    | admin    | admin123 |
    | user1    | pass123  |
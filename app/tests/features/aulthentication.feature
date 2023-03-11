Feature: Entering the correct authentication code
    As a user if I enter the correct authentication code I should be allowed to sign into the blog

Scenario: User has been sent to the authenticaiton page
    Given that I have recieved the authentication code 
    And I have entered the correct code into the field
    When I click submit 
    Then I should be able to see my blog homepage
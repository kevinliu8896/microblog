Feature: Laugh Button
   As a user, I want to be able to add a laugh to the laughing count for each review, if I find the review comedic in nature.

Scenario: User adds a laugh to a review
   Given that I am logged in to the Microblog application
   When I view a review that I find comedic
   Then I should see a "Laugh" button
   And when I click on the "Laugh" button
   Then the laughing count for the review should increase by 1

Scenario: User removes a laugh from a review
   Given that I am logged in to the Microblog application
   When I view a review that I previously laughed at
   Then I should see a "Laugh" button
   And when I click on the "Laugh" button
   Then the laughing count for the review should decrease by 1
Feature: Like Reviews
   As a user, I want to be able to like reviews so that I can show my support for them

Scenario: User likes a review
   Given that I am logged in to the Microblog application
   When I view a review
   Then I should see a "Like" button
   And when I click on the "Like" button
   Then the likes count for the review should increase by 1

Scenario: User unlikes a review
   Given that I am logged in to the Microblog application
   When I view a review that I previously liked
   Then I should see the "Like" button
   And when I click on the "Like" button
   Then the likes count for the review should decrease by 1
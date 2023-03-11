Feature: Dislike Reviews
   As a user, I want to be able to dislike reviews so that I can express my dissatisfaction with them

Scenario: User dislikes a review
   Given that I am logged in to the Microblog application
   When I view a review
   Then I should see a "Dislike" button
   And when I click on the "Dislike" button
   Then the dislikes count for the review should increase by 1


Scenario: User undislikes a review
   Given that I am logged in to the Microblog application
   When I view a review that I previously disliked
   Then I should see an "Dislike" button
   And when I click on the "Dislike" button
   Then the dislikes count for the review should decrease by 1
Feature: Archive Favourite Posts
  As a user, I want to be able to archive my favorite posts 
  so that I can keep them even if the original poster deletes the post.
  And, I want to keep my favourite list private and only visible to me.

Scenario: Add post to favorite list
  Given I am viewing a post on the website
  When I click on the "add to favorite" button
  Then the post should be added to my private favorite list

Scenario: Original poster deletes post
  Given I have added a post to my favorite list
  When the original poster deletes the post
  Then the post should still be visible in my private favorite list
  But the post should be deleted for all other users.

Scenario: Viewing favorite list
  Given I am logged in
  When I navigate to my favorite list
  Then I should be able to see all the posts I have added to my favorite list
  And no one else should be able to see the list without my permission.
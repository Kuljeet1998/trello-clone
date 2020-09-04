from django.test import TestCase
from .models import *
from django.contrib.auth.models import *
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
# Create your tests here.
# class UserTestCase(TestCase):

class BoardTests(APITestCase):
	def setUp(self):
		user=User.objects.create_user('foo', password='bar')
		user.is_superuser=False
		user.is_staff=True
		user.save()
		

		member=User.objects.create_user('john', password='doe')
		member.is_superuser=False
		member.is_staff=True
		member.save()
		
		Token.objects.create(user=user)

		Board.objects.create(title="First board",description="First board for testing",creator=user)
		board=Board.objects.first()
		board.members.add(user)
		board.members.add(member)
		

	def test_post_boards(self):

		user=User.objects.first()
		member=User.objects.last()

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		user_id=user.id
		member_id=member.id
		url=reverse("boards-list")
		
		data={"title":"test","description":"board for testing","creator":user_id,"members":[user_id,member_id]}
		response = client.post(url, data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		
		response_data=response.data
		all_keys=set(['id','creator_details','member_details','created','updated','title','description','creator','members'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_get_boards(self):
		
		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		url=reverse("boards-list")
		response=client.get(url)
		response_data=response.data['results'][0]
		all_keys=set(['id','creator_details','member_details','created','updated','title','description','creator','members'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_put_boards(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id
		url=reverse("boards-list")+str(board_id)+"/"

		user=User.objects.first()
		member=User.objects.last()
		user_id=user.id
		member_id=member.id
		
		data={"title":"test 1234","description":"board for testing","creator":user_id,"members":[user_id,member_id]}
		response=client.put(url,data)
		
		response_data=response.data
		
		board=Board.objects.last()
		
		all_keys=set(['id','creator_details','member_details','created','updated','title','description','creator','members'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)
		
		self.assertEqual(board.title,"test 1234")

	def test_patch_boards(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id
		url=reverse("boards-list")+str(board_id)+"/"
		
		user=User.objects.first()
		member=User.objects.last()
		user_id=user.id
		member_id=member.id

		data={"title":"test 1234!!"}
		response=client.patch(url,data)

		response_data=response.data
		
		board=Board.objects.last()
		
		all_keys=set(['id','creator_details','member_details','created','updated','title','description','creator','members'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

		self.assertEqual(board.title,"test 1234!!")

	def test_delete_boards(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id
		url=reverse("boards-list")+str(board_id)+"/"

		response=client.delete(url)
		self.assertEqual(response.status_code, 204)


class ListTests(APITestCase):
	
	def setUp(self):
		board_object=BoardTests()
		board_object.setUp()

		board=Board.objects.first()

		List.objects.create(title="List1",description="list1 for testing",board=board)

	def test_post_lists(self):

		user=User.objects.first()

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		user_id=user.id
		url=reverse("lists-list")
		board=Board.objects.first()
		
		data={"title":"test","description":"board for testing","board":str(board.id)}
		response = client.post(url, data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		
		response_data=response.data
		all_keys=set(['id','created','updated','title','description','board'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_get_lists(self):
		
		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		url=reverse("lists-list")
		response=client.get(url)
		response_data=response.data['results'][0]
		all_keys=set(['id','created','updated','title','description','board'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_put_boards(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id

		list=List.objects.last()
		list_id=list.id
		url=reverse("lists-list")+str(list_id)+"/"

		
		data={"title":"List1 123","description":"list1 for testing","board":board_id}
		response=client.put(url,data)
		
		response_data=response.data
		
		board=Board.objects.last()
		
		all_keys=set(['id','created','updated','title','description','board'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)
		
		list=List.objects.last()
		self.assertEqual(list.title,"List1 123")

	def test_patch_lists(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id
		list=List.objects.last()
		list_id=list.id
		url=reverse("lists-list")+str(list_id)+"/"

		data={"title":"test 1234!!"}
		response=client.patch(url,data)

		response_data=response.data
		
		all_keys=set(['id','created','updated','title','description','board'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

		list=List.objects.last()
		self.assertEqual(list.title,"test 1234!!")

	def test_delete_boards(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id
		list=List.objects.last()
		list_id=list.id
		url=reverse("lists-list")+str(list_id)+"/"

		response=client.delete(url)
		self.assertEqual(response.status_code, 204)


class CardTests(APITestCase):

	def setUp(self):
		list_object=ListTests()
		list_object.setUp()

		list=List.objects.last()
		Card.objects.create(title="Card1",description="card for testing", list=list)

	def test_post_lists(self):

		user=User.objects.first()

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		user_id=user.id
		url=reverse("cards-list")
		list=List.objects.first()
		
		data={"title":"card2","description":"card for testing","list":str(list.id)}
		response = client.post(url, data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		
		response_data=response.data
		all_keys=set(['id','created','updated','title','description','list','attachments'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_get_lists(self):
		
		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		url=reverse("cards-list")
		response=client.get(url)
		response_data=response.data['results'][0]
		all_keys=set(['id','created','updated','title','description','list','attachments'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_put_boards(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id

		list=List.objects.last()
		list_id=list.id
		card=Card.objects.last()
		card_id=card.id
		url=reverse("cards-list")+str(card_id)+"/"

		
		data={"title":"card2 123","description":"card for testing","list":str(list.id)}
		response=client.put(url,data)
		
		response_data=response.data
		
		board=Board.objects.last()
		
		all_keys=set(['id','created','updated','title','description','list','attachments'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)
		
		card=Card.objects.last()
		self.assertEqual(card.title,"card2 123")

	def test_patch_lists(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id
		list=List.objects.last()
		list_id=list.id
		card=Card.objects.last()
		card_id=card.id
		url=reverse("cards-list")+str(card_id)+"/"

		data={"title":"card 1234!!"}
		response=client.patch(url,data)

		response_data=response.data
		
		all_keys=set(['id','created','updated','title','description','list','attachments'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

		card=Card.objects.last()
		self.assertEqual(card.title,"card 1234!!")

	def test_delete_boards(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id
		list=List.objects.last()
		list_id=list.id
		card=Card.objects.last()
		url=reverse("cards-list")+str(card.id)+"/"

		response=client.delete(url)
		self.assertEqual(response.status_code, 204)


class CommentTests(APITestCase):

	def setUp(self):
		card_object=CardTests()
		card_object.setUp()

		Comment.objects.create(message="First comment",card=Card.objects.first(),user=User.objects.first())

	def test_post_lists(self):

		user=User.objects.first()

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		user_id=user.id
		url=reverse("comments-list")
		list=List.objects.first()
		
		card=Card.objects.last()

		data={"message":"this is a comment","card":str(card.id),"user":user_id}
		response = client.post(url, data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		
		response_data=response.data
		all_keys=set(['id','created','updated','message','card','user'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_get_lists(self):
		
		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		url=reverse("comments-list")
		response=client.get(url)
		response_data=response.data['results'][0]
		all_keys=set(['id','created','updated','message','card','user'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)

	def test_put_lists(self):

		token = Token.objects.get(user__username='foo')
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


		board=Board.objects.last()
		board_id=board.id

		list=List.objects.last()
		list_id=list.id
		card=Card.objects.last()
		card_id=card.id
		comment=Comment.objects.last()
		user=User.objects.last()
		url=reverse("comments-list")+str(comment.id)+"/"

		data={"message":"this is a comment 123","card":str(card.id),"user":user.id}
		response=client.put(url,data)
		
		response_data=response.data
		
		board=Board.objects.last()
		
		all_keys=set(['id','created','updated','message','card','user'])
		is_present=all_keys.issubset(response_data.keys())
		self.assertEqual(is_present,True)
		
		comment=Comment.objects.last()
		self.assertEqual(comment.message,"this is a comment 123")
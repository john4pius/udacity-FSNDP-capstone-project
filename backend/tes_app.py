import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Restaurant, Reservations, MenuItems


class CapstoneTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
                

        self.database_name = "movies"
        self.database_path = "postgres://demorole1:password1@localhost:5432/" + self.database_name
        setup_db(self.app, self.database_path)


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()




        self.manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtwNE8walZuX2pjT0pJbTRJSFBlRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaGFwcHlob3VyLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNzk0MjE1NzM5OTc0NTk0NTM1MiIsImF1ZCI6WyJmc25kY2Fwc3RvbmUiLCJodHRwczovL2ZzbmQtaGFwcHlob3VyLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODkwNTQ0MTgsImV4cCI6MTU4OTE0MDgxOCwiYXpwIjoiclkzZWU2eGpvV29jWFA3UGtDVW91SFM0OHZYOVlBb28iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnJlc3RhdXJhbnQiLCJnZXQ6bG9naW5fcmVzdWx0cyIsImdldDptZW51X2l0ZW0iLCJnZXQ6cmVzdGF1cmFudCIsInBhdGNoOnJlc3RhdXJhbnQiLCJwb3N0OnJlc3RhdXJhbnQiLCJyZWFkOnlvdXJzZWxmIl19.eI9z-amB1pnAAgtM6UPdTEz8P-5hVkMMktx45Cc7NW8VhD-kB0mWn3b0aMjJ3e6iOhPMfY23fAHDgAyCXUZQcgaC1yBV07b8zSlObOFYVZr6NwYSJClXgXezVBjS-JFIlKRDbHyWLfFTmEsVDGd8H61dwovPJDTz-xQYNgsDnff-tx8gDhvugnKWVXgR1j7AP3wOrAVt4lgnLYkPTf3PFfE37MDN6A75snTs9pLzT3F8me5CelOBbCyegtap6FRxJEbeildAVVzA5s08-VLud4OxemhgjscHmyWBZVhHlTA_EM8akfr_LUx94Fij1Hgvq4ET5yPoe5k2T8dzRE2Ugg'
        self.client = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtwNE8walZuX2pjT0pJbTRJSFBlRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaGFwcHlob3VyLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNjA2OTg0MzEzMDkzMzEwMDI5MSIsImF1ZCI6WyJmc25kY2Fwc3RvbmUiLCJodHRwczovL2ZzbmQtaGFwcHlob3VyLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODkwNTQ0OTIsImV4cCI6MTU4OTE0MDg5MiwiYXpwIjoiclkzZWU2eGpvV29jWFA3UGtDVW91SFM0OHZYOVlBb28iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmxvZ2luX3Jlc3VsdHMiLCJnZXQ6bWVudV9pdGVtIiwiZ2V0OnJlc3RhdXJhbnQiLCJwb3N0OnJlc2VydmF0aW9uIiwicmVhZDp5b3Vyc2VsZiJdfQ.abCpTLTu0w3U6DeBCtlWOarT7FpY8caSKsp6kzuyGSf1QN8KoBkPrg8MDl5_UcWZ3hbqK7vvBZulEKggZmJ5nUlVLVu60-0s3oS3UrJD3z1uKDZm6ZAPEPOHJ7xS3-TQeHq_P844Lk2aW25LXQoSAJjSnX2wIcyqdl0s4gwRJGUJoHCUU0EvHO96GHKq32miy75PrNNTe-xp9Rq5iRcdrbPtQoveFdgSSU4MgoEKyO516KYmo3x_kZLxGEphsWpBM0y1TJGqQczCtYfJmPzaHyl0Ia_4rOq8RpWLRvE01uH7FqdCgUzffh-M7SoQy3CKpMrLuWGnxPqZnp9G2BirUA'
        self.badtoken = 'badtoken'
        

        self.new_restaurant = {
            'name': 'Earls',
            'address': '5555 Street rd'
        }


        self.change_restaurant_address = {
            'address': '1111 Street rd'
        }


        self.reservation_info = {
            'time_of_res': "2020-08-19 18:30:00",
            'num_of_people': 5,
            'name_for_res': "Reservations Name"
        }    

       
        if Restaurant.query.filter(Restaurant.owner_id != 'badtoken').count() == 0:
            res = self.client().post('/restaurants', headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.new_restaurant)      
        self.current_rest_id = Restaurant.query.order_by(Restaurant.id.desc()).filter(Restaurant.owner_id != 'badtoken').first().id


        if Restaurant.query.filter(Restaurant.owner_id == 'badtoken').count() == 0:
            bad_token_rest = Restaurant(name="Bad name", address="bad address", owner_id="badtoken")
            bad_token_rest.insert()
        self.bad_rest_id = Restaurant.query.filter(Restaurant.owner_id == 'badtoken').first().id
        

        

    def tearDown(self):
        """Executed after each test"""        
        pass



    def test_homepage(self):       
        res = self.client().get('/')
        
        self.assertEqual(res.status_code, 200)


    def test_post_restaurant_with_valid_token(self):        
        res = self.client().post('/restaurants', headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.new_restaurant)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_401_post_restaurant_with_invalid_token(self):        
        res = self.client().post('/restaurants', headers={"Authorization": "Bearer {}".format(self.badtoken)}, json=self.new_restaurant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    


    def test_get_restaurants(self):        
        res = self.client().get('/restaurants')
        data = json.loads(res.data)

        restaurants = Restaurant.query.order_by(Restaurant.id).all()        
        output = [restaurant.format() for restaurant in restaurants]
       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['restaurants'], output)



    def test_get_restaurant_by_id(self):        
        res = self.client().get('/restaurants/' + str(self.current_rest_id))
        data = json.loads(res.data)

        restaurant = Restaurant.query.get(self.current_rest_id)
        format_rest = restaurant.format()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['restaurants'], format_rest)



    def test_patch_restaurant_by_id(self):               
        res = self.client().patch('/restaurants/' + str(self.current_rest_id), headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.change_restaurant_address)
        data = json.loads(res.data)
        
        restaurant = Restaurant.query.get(self.current_rest_id)
        format_rest = restaurant.format()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated_restaurant']['address'], self.change_restaurant_address['address'])


    
    def test_patch_restaurant_that_is_not_owners(self):               
        res = self.client().patch('/restaurants/' + str(self.bad_rest_id), headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.change_restaurant_address)
                      
        self.assertEqual(res.status_code, 401)



    def test_patch_restaurant_that_does_not_exist(self):               
        res = self.client().patch('/restaurants/' + str(self.current_rest_id + 1000), headers={"Authorization": "Bearer {}".format(self.manager)}, json=self.change_restaurant_address)
                      
        self.assertEqual(res.status_code, 422)



    def test_post_reservation_with_vaild_client(self):
        res = self.client().post('/restaurants/' + str(self.current_rest_id)  + '/reservation', headers={"Authorization": "Bearer {}".format(self.client)}, json=self.reservation_info)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)



    def test_post_reservation_with_invaild_client(self):
        res = self.client().post('/restaurants/' + str(self.current_rest_id)  + '/reservation', headers={"Authorization": "Bearer {}".format(self.badtoken)}, json=self.reservation_info)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)



    def test_post_reservation_with_non_existant_restaurant(self):
        res = self.client().post('/restaurants/' + str(self.current_rest_id + 1000)  + '/reservation', headers={"Authorization": "Bearer {}".format(self.client)}, json=self.reservation_info)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)

    
    
    def test_delete_restaurant_with_valid_owner(self):
        res = self.client().delete('/restaurants/' + str(self.current_rest_id), headers={"Authorization": "Bearer {}".format(self.manager)})
        
        deleted_rest = Restaurant.query.get(self.current_rest_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(deleted_rest, None)



    def test_delete_non_existant_restaurant(self):
        res = self.client().delete('/restaurants/' + str((self.current_rest_id + 10000)), headers={"Authorization": "Bearer {}".format(self.manager)})
        
        deleted_rest = Restaurant.query.get(self.current_rest_id + 10000)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(deleted_rest, None)
    

    


if __name__ == "__main__":
    unittest.main()
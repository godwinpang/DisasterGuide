//
//  SignupViewController.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class SignupViewController: UIViewController {

    @IBOutlet weak var nameField: UITextField!
    @IBOutlet weak var signUpButton: UIButton!
    
    let defaults = UserDefaults.standard
    
    override func viewDidLoad() {
        super.viewDidLoad()
        signUpButton.layer.cornerRadius = 5
        
        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(self.dismissKeyboard (_:)))
        self.view.addGestureRecognizer(tapGesture)
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func onSignUp(_ sender: Any) {
        
        let user_name = nameField.text ?? "Thomas"
        
        
        Alamofire.request(Constants().serverURL+"/getallusers").responseJSON { response in
            /*switch response.result {
             //get the JSON
             case .success(let value):
             let jsonString = JSON(value)
             print(jsonString)
             //returnArr = self.parseJSON(json: jsonString)
             case .failure(let error):
             print(error)
             returnArr = ["failure"]
             }
             */
            let jsonString = response.result.value
            print(jsonString)
            
        }
        
        let parameters: Parameters = [
            "first_name": user_name,
            "last_name": "Spencer",
            "birthday": [
                "month": 1,
                "day": 20,
                "year": 1998
            ],
            "role": "user"
        ]
        /*
        Alamofire.request(Constants().serverURL + "/adduser", method: .post, parameters: parameters, encoding: JSONEncoding.default).responseJSON { response in
            let jsonString = response.result as? String
            print(jsonString)
            let jsonObj = JSON(parseJSON: jsonString!)
            print(jsonObj["user_id"])
            let user_id = jsonObj["user_id"]
        }
        */
        
        
        self.performSegue(withIdentifier: "signUpSegue", sender: nil)
        
        //defaults.set(user_id, forKey: "user_id")
        defaults.set("user", forKey: "role")
        
        /*
        let username = nameField.text ?? "breaking"
        // TODO will trash if usernameString is empty
        firstly {
            SignupUtils.userSignIn(usernameString: username)
            }.done { _ in
                self.performSegue(withIdentifier: "signUpSegue", sender: nil)
            }.catch { error in
                // Handle Error
        }
        self.performSegue(withIdentifier: "signUpSegue", sender: nil)
         */
    }
    
    @objc func dismissKeyboard (_ sender: UITapGestureRecognizer) {
        nameField.resignFirstResponder()
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        
        //TODO http request to server
    }
    
    

}

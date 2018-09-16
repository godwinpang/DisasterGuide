//
//  SafeViewController.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON
import Foundation

class SafeViewController: UIViewController {
    
    @IBOutlet weak var hurricaneButton: UIButton!
    @IBOutlet weak var floodingButton: UIButton!
    @IBOutlet weak var earthquakeButton: UIButton!
    
    @IBAction func getRequest(_ sender: Any) {
        
        let disaster_longitude = -2.0
        let disaster_latitude = 12.8
        let disaster_radius = 5000.0
        print(getAllUsers(url: Constants().serverURL, disaster_longitude: disaster_longitude, disaster_latitude: disaster_latitude, disaster_radius: disaster_radius))
 
        //print(parseJSON(json: JSON(parseJSON: "{\"success\": \"true\",\"failure_reason\": \"None\",\"data\": [{\"first_name\": \"Jane\",\"last_name\": \"Doe\",\"age\": 37,\"latitude\": -2,\"longitude\": 12.9,\"status\": false},{\"first_name\": \"John\",\"last_name\": \"Smith\",\"age\": 28,\"latitude\": 12.3456,\"longitude\": -54.311,\"status\": false}]}"), disaster_longitude: disaster_longitude, disaster_latitude: disaster_latitude, disaster_radius: disaster_radius))
    }
    
    func getAllUsers(url: String, disaster_longitude: Double, disaster_latitude: Double, disaster_radius: Double) -> [String] {
        //Calculate Jacobian^2
        let C_sq = 24901.0*24901.0
        //The circumference of the earth squared in miles
        let sintheta = cos(3.41*disaster_latitude/180.0)
        
        let ds2_dphi2 = C_sq*sintheta*sintheta
        let ds2_dtheta2 = C_sq
        
        let disaster_radius_squared = disaster_radius*disaster_radius
        
        var returnArr = ["hi"]
        
        //Make POST request for all user locations
        Alamofire.request(url+"/getallusers").responseJSON { response in
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
        
        
        return returnArr
    }
    
    func parseJSON(json: JSON, disaster_longitude: Double, disaster_latitude: Double, disaster_radius: Double) -> [(Double?, Double?)] {
        var locations = [] as [(Double?, Double?)]
        //check if the request was successful
        //get location data and filter into location list
        
        for location in json["data"].arrayValue {
            let latitude = location["latitude"].double
            let longitude = location["longitude"].double
            //&& if let date_created = location["date_created"]
            //The earth is flat, especially since no one lives in antartica
            let Deltaphi = longitude!-disaster_longitude
            let Deltatheta = latitude!-disaster_latitude
            
            //Calculate Jacobian^2
            let C_sq = 24901.0*24901.0
            //The circumference of the earth squared in miles
            let sintheta = cos(3.41*disaster_latitude/180.0)
            
            let ds2_dphi2 = C_sq*sintheta*sintheta
            let ds2_dtheta2 = C_sq
            let disaster_radius_squared = disaster_radius*disaster_radius

            
            let distance_squared = ds2_dphi2*Deltaphi*Deltaphi + ds2_dtheta2*Deltatheta*Deltatheta
            if(distance_squared < disaster_radius_squared)
            {
                print("test")
                locations.append((latitude, longitude))
            }
        }
        
        return locations as! [(Double?, Double?)]
    }

    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        hurricaneButton.addBorder()
        floodingButton.addBorder()
        earthquakeButton.addBorder()
        
        self.navigationController?.isNavigationBarHidden = true

        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func toEarthquake(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(
            withIdentifier: "earthquake") as UIViewController!
        navigationController?.pushViewController(vc!, animated: true)
    }
    
    @IBAction func toFlooding(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(
            withIdentifier: "flooding") as UIViewController!
        navigationController?.pushViewController(vc!, animated: true)
    }
    
    @IBAction func toHurricane(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(
            withIdentifier: "hurricane") as UIViewController!
        navigationController?.pushViewController(vc!, animated: true)
    }
    
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}

//
//  DisasterViewController.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import UIKit
import GoogleMaps
import CoreLocation
import Alamofire
import SwiftyJSON

class DisasterViewController: UIViewController {

    @IBOutlet weak var disasterView: UIView!
    
    var mapView: GMSMapView?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let locationManager = CLLocationManager()
        
        locationManager.delegate = self
        // locationManager.requestAlwaysAuthorization()
        
        //locationManager.requestLocation()
        
        let camera = GMSCameraPosition.camera(withLatitude: 42.36, longitude: -71.09, zoom: 11.0)
        let gmsMapView = GMSMapView.map(withFrame: CGRect(x: 100, y: 200, width: 375, height: 667), camera: camera)
        do {
            if let styleURL = Bundle.main.url(forResource: "style", withExtension: "json") {
                gmsMapView.mapStyle = try GMSMapStyle(contentsOfFileURL: styleURL)
            } else {
                NSLog("Unable to find style.json")
            }
        } catch {
            NSLog("One or more of the map styles failed to load. \(error)")
        }
        
        let marker = GMSMarker()
        marker.position = CLLocationCoordinate2D(latitude: 42.36, longitude: -71.09)
        marker.title = "Sydney"
        marker.snippet = "Australia"
        marker.icon = GMSMarker.markerImage(with: UIColor.dGreen)
        marker.map = gmsMapView
        
        setAllMarkers(gmsMapView: gmsMapView)
        
        mapView = gmsMapView
        
        mapView?.center = self.view.center
        
        print(view.subviews.count)
        self.view.addSubview(mapView!)
        self.view.bringSubview(toFront: disasterView)
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func setAllMarkers(gmsMapView: GMSMapView) {
        Alamofire.request(Constants().serverURL+"/getallusers").responseJSON { response in
            
            let jsonString = response.result.value
            print(type(of: jsonString))
            print(jsonString)
            let markerParams = self.parseJSON(json: JSON(jsonString), disaster_longitude: 0, disaster_latitude: 0, disaster_radius: 0)
            for param in markerParams {
                self.generateMarker(param: param, gmsMapView: gmsMapView)
            }
        }
    }
    
    func generateMarker(param: (Double?, Double?, Int?, String?, String?), gmsMapView: GMSMapView) {
        let status = param.4 ?? "0"
        
        let marker = GMSMarker()
        marker.position = CLLocationCoordinate2D(latitude: param.0!, longitude: param.1!)
        marker.title = status
        marker.snippet = String(describing: param.2!)
        if (param.3! == "first_responder") {
            marker.icon = GMSMarker.markerImage(with: UIColor.dBlue)
        } else if (status == "false") {
            marker.icon = GMSMarker.markerImage(with: UIColor.dGreen)
        } else {
            marker.icon = GMSMarker.markerImage(with: UIColor.dRed)
        }
        //marker.icon = GMSMarker.markerImage(with: UIColor.dGreen)
        marker.map = gmsMapView
    }
    
    func parseJSON(json: JSON, disaster_longitude: Double, disaster_latitude: Double, disaster_radius: Double) -> [(Double?, Double?, Int?, String?, String?)] {
        var locations = [] as [(Double?, Double?, Int?, String?, String?)]
        //check if the request was successful
        //get location data and filter into location list
        
        for location in json["data"].arrayValue {
            let latitude = location["latitude"].double
            let longitude = location["longitude"].double
            //&& if let date_created = location["date_created"]
            //The earth is flat, especially since no one lives in antartica
            let age = location["age"].int
            let role = location["role"].string
            let status = String(describing: location["status"])
            
            print(status)
            print("result: " + String(status == "false"))
            
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
            
            locations.append((latitude, longitude, age, role, status))
        }
        
        return locations
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

extension UIViewController: CLLocationManagerDelegate {
    public func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        if let lat = locations.last?.coordinate.latitude, let long = locations.last?.coordinate.longitude {
            print("interesting")
            print("\(lat),\(long)")
        } else {
            print("No coordinates")
        }
    }
    public func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print(error)
    }
}

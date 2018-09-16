//
//  ViewController.swift
//  TestSpeechToText
//
//  Created by Geeling Chau on 9/15/18.
//  Copyright © 2018 Geeling Chau. All rights reserved.
//

import UIKit
import Speech

class ViewController: UIViewController {

    @IBOutlet weak var textLabel: UILabel!
    
    var isListening = false
    let audioEngine = AVAudioEngine()
    let speechRecognizer: SFSpeechRecognizer? = SFSpeechRecognizer()
    
    /// The current speech recognition request. Created when the user wants to begin speech recognition.
    var request = SFSpeechAudioBufferRecognitionRequest()
    var recognitionTask: SFSpeechRecognitionTask?
    private var myTimer: Timer?

    override func viewDidLoad() {
        super.viewDidLoad()
        self.requestTranscribePermissions()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // Button listener that toggles whether or not speech recognition should be happening.
    @IBAction func toggleS2T(_ sender: Any) {
        if(isListening) {
            isListening = false
            self.stopSpeechRecognition()
        } else {
            isListening = true
            self.recordAndRecognizeSpeech()
            
        }
        textLabel.text = "mwahahahahaha"
    }
    
    // Checks whether or no the app has access to transcribe speech.
    func requestTranscribePermissions() {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                if authStatus == .authorized {
                    print("Good to go!")
                } else {
                    print("Transcription permission was declined.")
                }
            }
        }
    }
    
    
    // Stops and clears any speech recognition.
    func stopSpeechRecognition() {
        // Release audio engine resources
        audioEngine.stop()
        request.endAudio()
        recognitionTask?.cancel()
        
        if(!self.isListening) {
            self.myTimer?.invalidate()
        }
    }
    
    // Creates and initializes the objects needed to do speech recognititon.
    func recordAndRecognizeSpeech() {
        
        // Creates the request to recognize speech with audio buffer.
        request = SFSpeechAudioBufferRecognitionRequest()
        
        // Install sound input to bus 0.
        let node = audioEngine.inputNode
        
        let recordingFormat = node.outputFormat(forBus:0)
        node.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in self.request.append(buffer)
        }
        
        // Prepare and start audio engine.
        audioEngine.prepare()
        do {
            try audioEngine.start()
        } catch {
            return print(error)
        }
        
        // Create your recognizer.
        guard let myRecognizer = SFSpeechRecognizer() else { return }
        
        if !myRecognizer.isAvailable {
            return
        }
        
        // Create the recognition task with the recognizer.
        recognitionTask = speechRecognizer?.recognitionTask(with: request, resultHandler: { result, error in
            // Update on-screen text with best transcription string.
            if let result = result {
                let bestString = result.bestTranscription.formattedString
                self.textLabel.text = bestString
                
            }
            // Otherwise, if an error is found, remove the listen bind.
            else if let error = error {
                if result?.isFinal ?? (error != nil) {
                    node.removeTap(onBus: 0)
                }
                print(error)
                
            }})
        
        print("first hi")
        self.myTimer?.invalidate()
        self.myTimer = Timer.scheduledTimer(timeInterval: 50.0, target: self, selector: #selector("self.continueSpeechRecognition"), userInfo: nil, repeats: false)
        print("second hi")

        
        
    }
    
    // To be called on a 50 second interval to bypass the ~1 min timeout. 
    func continueSpeechRecognition() {
        print("third hi")
        self.stopSpeechRecognition()
        self.recordAndRecognizeSpeech()
    }
    
    
}


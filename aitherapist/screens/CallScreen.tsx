import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Alert, ScrollView } from 'react-native';
import { FontAwesome } from '@expo/vector-icons'; 
import * as Speech from 'expo-speech';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../App';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

interface Props {
  navigation: HomeScreenNavigationProp;
}

const CallScreen: React.FC<Props> = ({ navigation }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcribedText, setTranscribedText] = useState('');

  useEffect(() => {
    const speech = 'Welcome to Therapist AI. The session is now starting. How was your day?';
    Speech.speak(speech, {language: 'en-US'});
  }, []);

  const listenInBackend = async () => {
    try {
      const serverResponse = await fetch('http://localhost:5001/listen', {
        method: 'get'
      });
  
      const data = await serverResponse.json();
      setTranscribedText(data.response);
      console.log(data.response)
      await Speech.speak(data.response, {language: 'en-US'})
    } catch (error) {
      Alert.alert('Error', 'Failed to transcribe audio');
      console.error(error);
    }
  };

  const endCall = () => {
    Speech.speak('Thank you for using Therapist AI.', {
      language: 'en-US',
    });
    navigation.navigate('Home');
  };

  return (
    <View style={styles.container}>
      <Image source={require('../data/images/aitherapist.jpg')} style={styles.image} />
      <Text style={styles.title}>Therapist.AI</Text>
      <Text style={styles.status}>{isRecording ? 'Recording...' : 'Tap microphone to speak'}</Text>
      
      <ScrollView style={styles.transcriptionContainer}>
        {transcribedText ? (
          <Text style={styles.transcriptionText}>{transcribedText}</Text>
        ) : null}
      </ScrollView>
      
      <View style={styles.bottomContainer}>
        <View style={styles.controlsContainer}>
          <TouchableOpacity 
            onPress={listenInBackend}
            style={styles.actionButton}
          >
            <FontAwesome 
              name={isRecording ? "microphone-slash" : "microphone"} 
              size={30} 
              color="#fff" 
            />
            <Text style={styles.actionText}>
              {isRecording ? 'Stop' : 'Record'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={endCall} style={styles.endCallButton}>
            <FontAwesome name="phone" size={30} color="#fff" />
            <Text style={styles.transcriptionText}>End call</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2f4f82', 
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingTop: 40,
  },
  image: {
    width: 150,
    height: 150,
    borderRadius: 75,
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  status: {
    fontSize: 16,
    color: '#cfcfcf',
    marginBottom: 20,
  },
  bottomContainer: {
    position: 'absolute',
    bottom: 20,
    width: '100%',
    alignItems: 'center',
  },
  controlsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 20,
  },
  actionsContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  actionButton: {
    alignItems: 'center',
  },
  actionText: {
    color: '#fff',
    marginTop: 10,
    fontSize: 14,
  },
  endCallButton: {
    backgroundColor: '#e74c3c',
    paddingVertical: 15,
    paddingHorizontal: 50,
    borderRadius: 30,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  transcriptionContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    padding: 15,
    borderRadius: 10,
    width: '80%',
    maxHeight: '40%',
    marginBottom: 120,
  },
  transcriptionText: {
    color: '#fff',
    fontSize: 16,
  },
});

export default CallScreen;
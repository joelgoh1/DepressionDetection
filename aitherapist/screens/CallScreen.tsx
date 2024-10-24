// screens/CallScreen.tsx
import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { FontAwesome } from '@expo/vector-icons'; 
import * as Speech from 'expo-speech';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../App';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

type Props = {
  navigation: HomeScreenNavigationProp;
};

const CallScreen: React.FC<Props> = ({ navigation }) => {
  const therapistImage = require('../data/images/aitherapist.jpg');

  useEffect(() => {
    const speech = 'Welcome to Therapist AI. The session is now starting. How was your day?';
    Speech.speak(speech, {language: 'en-US'});
  }, []);

  const endCall = () => {
    // Speak a message when the call is ended
    Speech.speak('Ending the call. Thank you for using Therapist AI.', {
      language: 'en-US',
    });
    navigation.navigate('Home');
    
  };
  return (
    <View style={styles.container}>
      <Image source={therapistImage} style={styles.image} />
      <Text style={styles.title}>Therapist.AI</Text>
      <Text style={styles.status}>Listening...</Text>
      
      <View style={styles.actionsContainer}>
        <TouchableOpacity style={styles.actionButton}>
          <FontAwesome name="microphone-slash" size={30} color="#fff" />
          <Text style={styles.actionText}>Mute</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton}>
          <FontAwesome name="file-text" size={30} color="#fff" />
          <Text style={styles.actionText}>Transcribe</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity onPress={endCall} style={styles.endCallButton}>
        <FontAwesome name="phone" size={30} color="#fff" />
        <Text style={styles.endCallText}>End call</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#2f4f82', 
    alignItems: 'center',
    justifyContent: 'center',
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
    marginBottom: 40,
  },
  actionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '60%',
    marginBottom: 40,
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
  endCallText: {
    color: '#fff',
    marginLeft: 10,
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default CallScreen;

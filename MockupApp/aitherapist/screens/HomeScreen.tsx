import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../App';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

type Props = {
  navigation: HomeScreenNavigationProp;
};

const HomeScreen: React.FC<Props> = ({ navigation }) => {
  const therapistImage = require('../data/images/aitherapist.jpg');
  return (
    <View style={styles.container}>
      <Image
        source={ therapistImage } 
        style={styles.image}
      />
      <Text style={styles.description}>Talk live with a therapist</Text>
      <TouchableOpacity onPress={() => navigation.navigate('Call')} style={styles.callButton}>
        <Text style={styles.callButtonText}>Call now</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    width: 200,
    height: 200,
    borderRadius: 600,
    marginTop: '-40%',
    marginBottom: 20,
  },
  description: {
    fontSize: 35,
    fontWeight: 'bold',
    marginBottom: 40,
    textAlign: 'center',
  },
  callButton: {
    backgroundColor: '#D9D9D9',
    paddingVertical: 20,
    paddingHorizontal: 40,
    borderRadius: 15,
  },
  callButtonText: {
    fontSize: 24,
    fontWeight: 'bold',
  },
});

export default HomeScreen;

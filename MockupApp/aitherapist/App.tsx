// App.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './screens/HomeScreen';
import CallScreen from './screens/CallScreen';


export type RootStackParamList = {
  Home: undefined;
  Call: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen 
          name="Home" 
          component={HomeScreen} 
          options={{
            title: 'Therapist.AI',
            headerStyle: {
              backgroundColor: '#3a59b7',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontSize: 24,
              fontWeight: 'bold',
            },
          }}
        />
        <Stack.Screen 
          name='Call' 
          component={CallScreen} 
          options = {{
            headerShown: false
          }}
          />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
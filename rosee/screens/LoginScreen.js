import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';

const LoginScreen = ({ navigation }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
        <View style={styles.container}>
            <View style={styles.logoContainer}>
                <View style={styles.logoIcon}>
                <Image source={require('../assets/icon.png')}style={styles.iconContainer}></Image>
                </View>
                <Text style={styles.logoText}>ROSEE</Text>
                <Text style={styles.logoSubText}>THRIFT APP</Text>
            </View>
            <TextInput
                style={styles.input}
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
            />
            <TextInput
                style={styles.input}
                placeholder="Password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />
            <View style={styles.optionsContainer}>
                <TouchableOpacity>
                    <Text style={styles.optionText}>Remember Me</Text>
                </TouchableOpacity>
                <TouchableOpacity>
                    <Text style={styles.optionText}>Forgot Password?</Text>
                </TouchableOpacity>
            </View>
            <TouchableOpacity style={styles.loginButton}>
                <Text style={styles.loginButtonText}>Login</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => navigation.navigate('Register')}>
                <Text style={styles.registerText}>Don’t have an account? <Text style={styles.registerLink}>Create an account</Text></Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'grey',
        paddingHorizontal: 20,
        justifyContent: 'center',
    },
    logoContainer: {
        alignItems: 'center',
        marginBottom: 40,
    },
    logoIcon: {
        // Style for your SVG/Image
        marginBottom: 10,
    },
    logoText: {
        fontSize: 36,
        fontWeight: 'bold',
        color: '#d32f2f',
    },
    logoSubText: {
        fontSize: 18,
        color: '#d32f2f',
    },
    input: {
        backgroundColor: '#ececec',
        padding: 15,
        borderRadius: 8,
        marginBottom: 15,
    },
    optionsContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 30,
    },
    optionText: {
        color: '#808080',
    },
    loginButton: {
        backgroundColor: '#d32f2f',
        paddingVertical: 15,
        borderRadius: 8,
        alignItems: 'center',
        marginBottom: 20,
    },
    loginButtonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    registerText: {
        textAlign: 'center',
        color: '#808080',
    },
    registerLink: {
        color: '#0000EE',
        fontWeight: 'bold',
    },
});

export default LoginScreen;

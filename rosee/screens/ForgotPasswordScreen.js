import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';

const ForgotPasswordScreen = ({ navigation }) => {
    const [email, setEmail] = useState('');

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity onPress={() => navigation.goBack()}>
                <Image source={require('../assets/back.png')}style={styles.logoIcon}></Image>
                </TouchableOpacity>
                <Text style={styles.headerText}>FORGOT PASSWORD</Text>
                <TouchableOpacity>
                <Image source={require('../assets/menu.png')}style={styles.logoIcon}></Image>
                </TouchableOpacity>
            </View>
            <View style={styles.iconContainer}>
            <Image source={require('../assets/fp.png')}style={styles.iconContainer}></Image>
            </View>
            <Text style={styles.helpText}>Trouble Logging in?</Text>
            <Text style={styles.subText}>Enter your email and we'll send you a link to reset your password.</Text>
            <TextInput
                style={styles.input}
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
            />
            <TouchableOpacity style={styles.resetButton}>
                <Text style={styles.resetButtonText}>Reset Password</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => navigation.navigate('Login')}>
                <Text style={styles.returnText}>Return to Login Page</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f4f4f4',
        paddingHorizontal: 20,
        justifyContent: 'center',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 20,
        backgroundColor: '#d32f2f',
        paddingVertical: 10,
        paddingHorizontal: 15,
        borderRadius: 8,
    },
    headerText: {
        fontSize: 24,
        color: '#fff',
        fontWeight: 'bold',
    },
    iconContainer: {
        alignItems: 'center',
        marginBottom: 20,
    },
    helpText: {
        fontSize: 18,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 10,
    },
    subText: {
        fontSize: 14,
        textAlign: 'center',
        marginBottom: 30,
    },
    input: {
        backgroundColor: '#fff',
        padding: 15,
        borderRadius: 8,
        marginBottom: 20,
    },
    resetButton: {
        backgroundColor: '#d32f2f',
        paddingVertical: 15,
        borderRadius: 8,
        alignItems: 'center',
        marginBottom: 20,
    },
    resetButtonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    returnText: {
        textAlign: 'center',
        color: '#808080',
    },
});

export default ForgotPasswordScreen;

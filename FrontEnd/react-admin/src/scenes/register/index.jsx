import React, {useEffect, useState} from 'react';
import {Container, Typography, TextField, Button, useTheme, Box, FormControl} from "@mui/material";
import {tokens} from "../../theme";
import {useNavigate} from "react-router-dom";
import config from "../../config.json";
import axios from "axios";


const Register = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [name, setName] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false)

    let navigate = useNavigate();

    useEffect(() => {
        setError(null)
    }, [email, password])
    const register = async () => {
        if (loading) {
            return
        }
        if (!email || !password || !confirmPassword) {
            return setError("You must fill in all credentials.")
        }
        if(password !== confirmPassword)
        {
            return setError("Password and Confirm Password don't match")
        }
        try {
            console.log({
                email: email,
                password: password
            })
            console.log(config.url);
            const response = await axios.post(`${config.url}/user/register`,
                {
                    email: email,
                    password: password,
                    name: name
                });
            localStorage.setItem("confirm", JSON.stringify(response.data));
            navigate("/confirm");
        } catch (error) {
            console.log(error)
            setLoading(false)
            setError(error.response.data)
        }
    }
    const registerContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
    };

    const registerFormStyle = {
        display: 'flex',
        flexDirection: 'column',
        width: 300,
    };

    const formGroupStyle = {
        marginBottom: 20,
    };

    const registerBtnStyle = {
        marginTop: 16,
        color: colors.primary[500],
        fontSize: 20,
        fontWeight: "bold",
        backgroundColor: colors.greenAccent[400]
    };
    return (
        <Container style={registerContainerStyle}>
            <Typography variant="h5" component="h2" gutterBottom>
                Create an Account
            </Typography>
            <FormControl fullWidth sx={{
                '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                        borderColor: colors.grey[400],
                    },
                    '&.Mui-focused fieldset': {
                        borderColor: colors.grey[400],
                    },
                },
                '& .MuiInputLabel-outlined.Mui-focused': {
                    color: colors.grey[100],
                }
            }} style={registerFormStyle}>
                <Box style={formGroupStyle}>
                    <TextField label="Name" fullWidth onChange={(e) => setName(e.target.value)}/>
                </Box>
                <Box style={formGroupStyle}>
                    <TextField label="Email" type="email" fullWidth onChange={(e) => setEmail(e.target.value)}/>
                </Box>
                <Box style={formGroupStyle}>
                    <TextField label="Password" type="password" fullWidth onChange={(e) => setPassword(e.target.value)}/>
                </Box>
                <Box style={formGroupStyle}>
                    <TextField label="Confirm Password" type="password" fullWidth onChange={(e) => setConfirmPassword(e.target.value)}/>
                </Box>
                {error?<Typography color={'#eb6157'} style={{textAlign: "center"}}>{error}</Typography>: null}
                <Button
                    variant="contained"
                    size="large"
                    style={registerBtnStyle}
                    onClick={register}
                >
                    Register
                </Button>
            </FormControl>
        </Container>
    );
};

export default Register;
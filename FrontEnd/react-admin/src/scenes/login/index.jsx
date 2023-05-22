import React, {useEffect, useState, useContext } from 'react';
import {Container, Typography, TextField, Button, useTheme, Box, FormControl} from "@mui/material";
import {tokens} from "../../theme";
import {useNavigate} from "react-router-dom";
import config from "../../config.json";
import axios from "axios";
import Authcontext from '../../components/AuthContext';


const Login = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false)
    const {setIsAuthenticated, setName } = useContext(Authcontext);

    let navigate = useNavigate();

    useEffect(() => {
        setError(null)
    }, [email, password])
    const login = async () => {
        if (loading) {
            return
        }
        if (!email || !password) {
            return setError("You must fill in all credentials.")
        }
        try {
            console.log({
                email: email,
                password: password
            })
            console.log(config.url);
            const response = await axios.post(`${config.url}/user/login`,
                {
                    email: email,
                    password: password
                });
            localStorage.setItem("user", JSON.stringify(response.data));
            setIsAuthenticated(true);
            setName(response.data.name)
            navigate("/");
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

    const loginBtnStyle = {
        marginTop: 16,
        color: colors.primary[500],
        fontSize: 20,
        fontWeight: "bold",
        backgroundColor: colors.greenAccent[400]
    };
    return (
        <Container style={registerContainerStyle}>
            <Typography variant="h4" component="h2" gutterBottom>
                Login
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
                    <TextField label="Email" type="email" fullWidth onChange={(e) => setEmail(e.target.value)}/>
                </Box>
                <Box style={formGroupStyle}>
                    <TextField label="Password" type="password" fullWidth onChange={(e) => setPassword(e.target.value)}/>
                </Box>
                {error?<Typography color={'#eb6157'} style={{textAlign: "center"}}>{error}</Typography>: null}
                <Button
                    variant="contained"
                    size="large"
                    style={loginBtnStyle}
                    onClick={login}
                >
                    Login
                </Button>
            </FormControl>
        </Container>
    );
};

export default Login;
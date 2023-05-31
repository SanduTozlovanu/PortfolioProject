import React, {useEffect, useState} from 'react';
import {Container, Typography, TextField, Button, useTheme, Box, FormControl, IconButton} from "@mui/material";
import RefreshIcon from '@mui/icons-material/Refresh';
import {tokens} from "../../theme";
import {useNavigate} from "react-router-dom";
import config from "../../config.json";
import axios from "axios";


const Confirm = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [code, setCode] = useState("");
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false)

    let navigate = useNavigate();

    useEffect(() => {
        let user = localStorage.getItem("confirm");
        console.log(user)
        if (!user) {
            navigate("/login")
            return
        }
        user = JSON.parse(user)
        setEmail(user.email)
    }, [])
    const confirm = async () => {
        if (loading) {
            return
        }
        if (!code) {
            return setError("You must fill in the code.")
        }
        try {
            await axios.post(`${config.url}/user/confirm`,
                {
                    code: code,
                    email: email
                });
            localStorage.removeItem("confirm");
            navigate("/login");
        } catch (error) {
            setLoading(false)
            setError(error.response.data)
        }
    }
    const reSend = async () => {
        if (loading) {
            return
        }
        try {
            await axios.post(`${config.url}/user/confirm/resend`,
                {
                    email: email
                });
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
        display: "flex",
        flexDirection: 'row',
        marginBottom: 20
    };

    const registerBtnStyle = {
        marginTop: 16,
        color: colors.primary[500],
        fontSize: 20,
        width: '88%',
        fontWeight: "bold",
        backgroundColor: colors.greenAccent[400]
    };
    return (
        <Container style={registerContainerStyle}>
            <Typography variant="h3" component="h2" gutterBottom marginBottom={8}>
                We have sent you an email containing the confirmation code to your email. Enter it in the field above
                please.
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
                    <TextField label="Code" style={{width: '100%'}} fullWidth
                               onChange={(e) => setCode(e.target.value)}/>
                    <IconButton onClick={reSend}>
                        <RefreshIcon/>
                    </IconButton>
                </Box>
                {error ? <Typography color={'#eb6157'} style={{textAlign: "center"}}>{error}</Typography> : null}
                <Button
                    variant="contained"
                    size="large"
                    style={registerBtnStyle}
                    onClick={confirm}
                >
                    Send
                </Button>
            </FormControl>
        </Container>
    );
};

export default Confirm;
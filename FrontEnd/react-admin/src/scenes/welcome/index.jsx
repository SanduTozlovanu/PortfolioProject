import React from 'react';
import {Container, Typography, Button, useTheme, Box} from "@mui/material";
import {tokens} from "../../theme";
import {useNavigate} from "react-router-dom";


const Welcome = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    let navigate = useNavigate();
    const registerContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
    };

    const formGroupStyle = {
        display: "flex",
        flexDirection: 'row',
        marginBottom: 20
    };

    const loginBtnStyle = {
        margin: 16,
        color: colors.primary[500],
        fontSize: 20,
        fontWeight: "bold",
        backgroundColor: colors.blueAccent[200]
    };
    const registerBtnStyle = {
        margin: 16,
        color: colors.primary[500],
        fontSize: 20,
        fontWeight: "bold",
        backgroundColor: colors.greenAccent[400]
    };
    return (
        <Container style={registerContainerStyle}>
            <Typography variant="h3" component="h2" gutterBottom marginBottom={8}>
                We are thrilled that you've chosen us to help you manage your stock investitions.
                With our user-friendly interface and intuitive features, you can easily analyse stocks, their financial data, be up to date to the stock news
                , manage your portfolio and use our Portfolio generator that uses different investing strategies and technologies.
            </Typography>
            <Box style={formGroupStyle}>
                <Button variant="contained" size="large" style={loginBtnStyle} onClick={() => navigate('/login')}>
                    Login
                </Button>
                <Button variant="contained" size="large" style={registerBtnStyle} onClick={() => navigate('/register')}>
                    Register
                </Button>
            </Box>
        </Container>
    );
};

export default Welcome;
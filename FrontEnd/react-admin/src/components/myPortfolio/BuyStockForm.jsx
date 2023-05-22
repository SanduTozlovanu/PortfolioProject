import React, {useEffect, useState} from 'react';
import {
    Dialog,
    DialogContent,
    DialogTitle,
    Box,
    TextField,
    Autocomplete,
    DialogActions,
    Button,
    Grid,
    useTheme, Typography, Divider
} from '@mui/material';
import axios from "axios";
import config from "../../config.json";
import {tokens} from "../../theme";

function BuyStockForm({open, onClose}) {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [selectedOption, setSelectedOption] = useState(null);
    const [ticker, setTicker] = useState("");
    const [price, setPrice] = useState("");
    const [quantity, setQuantity] = useState(1);
    const [error, setError] = useState("");
    const [options, setOptions] = useState([]);

    useEffect(() => {
        getOptions()
    }, []);

    const getOptions = async () => {
        try {
            const response = await axios.get(`${config.url}/stock/select`);
            setOptions(response.data)
            setError("")
        } catch (error) {
            console.log(error)
            setError(error.response.data)
        }
    }

    const buyStocks = async () => {
        if(!ticker || !price)
        {
            setError("You must select the stock first")
            return
        }
        if(!quantity)
        {
            setError("You must select the quantity first")
            return
        }

        try {
            await axios.post(`${config.url}/portfolio/stock/buy`,
                {
                    ticker: ticker,
                    price: price,
                    quantity: quantity
                },
                {
                    headers: {
                        Authorization: JSON.parse(localStorage.getItem("user")).token,
                    }

                }
            );
            setError("")
            window.location.reload();
        } catch (error) {
            console.log(error)
            setError(error.response.data)
        }
    }
    const handleOptionChange = (event, value) => {
        setSelectedOption(value);
        if (value) {
            setTicker(value.value)
            setPrice(value.price)
        } else {
            setTicker(null)
            setPrice(null)
        }
    };

    const handleQuantityChange = (event) => {
        const inputValue = event.target.value;

        // Remove non-numeric characters using a regular expression
        const sanitizedValue = inputValue.replace(/[^0-9]/g, '');
        if (sanitizedValue)
            setQuantity(parseInt(sanitizedValue));
        else
            setQuantity(null);
    };
    return (
        <Dialog open={open} onClose={onClose} fullWidth>
            <DialogTitle style={{textAlign: 'center', fontSize: 24, backgroundColor: colors.primary[400]}}>Buy
                Stock</DialogTitle>
            <DialogContent style={{backgroundColor: colors.primary[400]}}>
                <Box style={{margin: 20}}>
                    <Grid container spacing={3}>
                        <Grid item xs={6} md={6}>
                            <Autocomplete
                                value={selectedOption}
                                onChange={handleOptionChange}
                                options={options}
                                getOptionLabel={(option) => option.label}
                                renderOption={(props, option) => (
                                    <Box component="li" sx={{'& > img': {mr: 2, flexShrink: 0}}} {...props}>
                                        <img
                                            loading="lazy"
                                            width="20"
                                            src={`https://financialmodelingprep.com/image-stock/${option.value}.png`}
                                            alt=""
                                        />
                                        {option.label} ({option.value})
                                    </Box>
                                )}
                                renderInput={(params) => <TextField {...params} label="Select Stock to buy"/>}
                            />
                        </Grid>
                        <Grid item xs={6} md={6}>
                            <Typography variant="h4" style={{textAlign: 'center'}}> Price per share </Typography>
                            <Typography variant="h4" style={{
                                textAlign: 'center',
                                color: colors.greenAccent[400]
                            }}> {price}$ </Typography>
                        </Grid>
                        <Grid item xs={12} md={12}>
                            <Divider orientation="horizontal" color={colors.primary[100]}/>
                        </Grid>
                        <Grid item xs={6} md={6}>
                            <TextField style={{width: "100%"}}
                                       label="Number of Shares to buy"
                                       value={quantity}
                                       onChange={handleQuantityChange}
                                       type="tel"
                            />

                        </Grid>
                        <Grid item xs={6} md={6}>
                            <Typography variant="h4" style={{textAlign: 'center'}}> Total price </Typography>
                            <Typography variant="h4" style={{
                                textAlign: 'center',
                                color: colors.greenAccent[400]
                            }}> {(quantity * price).toFixed(2)}$ </Typography>
                        </Grid>
                        {error ? (
                            <Grid item xs={12} md={12}>
                                <Typography color={'#eb6157'} style={{textAlign: "center"}}>{error}</Typography>
                            </Grid>
                        ) : null}
                    </Grid>
                </Box>
            </DialogContent>
            <DialogActions style={{backgroundColor: colors.primary[400]}}>
                <Button onClick={onClose} sx={{
                    backgroundColor: colors.redAccent[400],
                    ":hover": {backgroundColor: colors.redAccent[700]}
                }}>
                    Close
                </Button>
                <Button onClick={buyStocks} sx={{
                    backgroundColor: colors.greenAccent[400],
                    ":hover": {backgroundColor: colors.greenAccent[700]}
                }}>
                    Buy
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default BuyStockForm;
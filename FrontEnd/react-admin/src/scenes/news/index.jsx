import {Box, CircularProgress, Grid, Pagination , useTheme} from "@mui/material";
import {tokens} from "../../theme";
import { useNavigate } from 'react-router-dom';
import React, {useState, useEffect} from "react";
import config from "../../config.json";
import axios from "axios";
import Topbar from "../global/Topbar";
import NewsComponent from "../../components/NewsComponent";

const News = () => {
    const componentsPerPage = 4;
    const [totalComponents, setTotalComponents] = useState(0);
    const [news, setNews] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const startIndex = (currentPage - 1) * componentsPerPage;
    const endIndex = startIndex + componentsPerPage;

    const visibleNews = news.slice(startIndex, endIndex);

    const handlePageChange = (event, page) => {
        setCurrentPage(page);
    };

    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    useEffect(() => {
        getNews()
    }, []);


    const getNews = async () => {
        try{
            const user = JSON.parse(localStorage.getItem("user"))
            let response
            if (user)
            {
                response = await axios.get(`${config.url}/news`, {
                headers: {
                    Authorization: user.token,
                },
            });
            }
            else
            {
                response = await axios.get(`${config.url}/news`);
            }
            setNews(response.data)
            setTotalComponents(response.data.length)
            setIsLoading(false);
        } catch(error){
            console.log(error)
            setIsLoading(false);
        }
    }

    if (isLoading) {
        return (
            <Box sx={{ display: 'flex', justifyContent:"center", alignItems:"center", height:"100vh"}}>
                <CircularProgress sx={{color: colors.primary[300]}} />
            </Box>
        );
    }
    return (
        <Box m="20px">
            <Topbar title="NEWS" subtitle="Find out about the hottest stock news" ticker={'news'} isTicker={false}/>
            <Grid container spacing={1}>
                {visibleNews.map((item, index) => (
                    <Grid item xs={6} md={6} key={index}>
                        <NewsComponent news={item}/>
                    </Grid>
                ))}
            </Grid>
            <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
                <Pagination
                    count={Math.ceil(totalComponents / componentsPerPage)}
                    page={currentPage}
                    onChange={handlePageChange}
                />
            </Box>
        </Box>
    );
};

export default News;

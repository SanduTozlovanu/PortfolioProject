import React, {useState} from "react";
import {Navigate, Route, Routes} from "react-router-dom";
import Sidebar from "./scenes/global/Sidebar";
import StockScreener from "./scenes/stockScreener";
import Line from "./scenes/line";
import Pie from "./scenes/pie";
import {CssBaseline, ThemeProvider} from "@mui/material";
import {ColorModeContext, useMode} from "./theme";
import StockProfile from "./scenes/stockProfile";
import Welcome from "./scenes/welcome";
import Register from "./scenes/register";
import Confirm from "./scenes/confirm";
import Login from "./scenes/login";
import AuthContext from './components/AuthContext';
import MyPortfolio from "./scenes/myPortfolio";
import News from "./scenes/news";
import TransactionHistory from "./scenes/transactionHistory";
import PortfolioCreator from "./scenes/portfolioCreator";
import PortfolioScreener from "./scenes/portfolioScreener";

function App() {
    const [theme, colorMode] = useMode();
    const [name, setName] = useState(() => {
        let user = JSON.parse(localStorage.getItem("user"))
        if (!user)
            return ""
        return user.name
    });
    const [isCollapsed, setIsCollapsed] = useState(false)
    const [isAuthenticated, setIsAuthenticated] = useState(!!(localStorage.getItem("user")));
    const handleToggleCollapse = (collapsed) => {
        setIsCollapsed(!collapsed)
    };


    return (
        <AuthContext.Provider value={{isAuthenticated, setIsAuthenticated, name, setName}}>
            <ColorModeContext.Provider value={colorMode}>
                <ThemeProvider theme={theme}>
                    <CssBaseline/>
                    <div className="app">
                        <Sidebar onToggleCollapse={handleToggleCollapse}/>
                        <main className="content" style={{marginLeft: `${isCollapsed ? 80 : 270}px`}}>
                            <Routes>
                                <Route path="/" element={isAuthenticated ? (<Navigate to="/myPortfolio" replace/>) : (<Navigate to="/welcome" replace/>)}/>
                                <Route path="/myPortfolio" element={isAuthenticated ? (<MyPortfolio/>) : (<Navigate to="/login" replace/>)}/>
                                <Route path="/transactions" element={isAuthenticated ? (<TransactionHistory/>) : (<Navigate to="/login" replace/>)}/>
                                <Route path="/portfolioCreator" element={isAuthenticated ? (<PortfolioCreator/>) : (<Navigate to="/login" replace/>)}/>
                                <Route path="/stockProfile/:stock_name" element={<StockProfile/>}/>
                                <Route path="/portfolioScreener/:strategy_name" element={isAuthenticated ? (<PortfolioScreener/>) : (<Navigate to="/login" replace/>)}/>
                                <Route path="/welcome" element={<Welcome/>}/>
                                <Route path="/register" element={<Register/>}/>
                                <Route path="/confirm" element={<Confirm/>}/>
                                <Route path="/login" element={<Login/>}/>
                                <Route path="/stockScreener" element={<StockScreener/>}/>
                                <Route path="/pie" element={<Pie/>}/>
                                <Route path="/line" element={<Line/>}/>
                                <Route path="/news" element={<News/>}/>
                            </Routes>
                        </main>
                    </div>
                </ThemeProvider>
            </ColorModeContext.Provider>
        </AuthContext.Provider>
    );
}

export default App;

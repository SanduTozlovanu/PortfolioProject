import React, {useState} from "react";
import {Navigate, Route, Routes} from "react-router-dom";
import Sidebar from "./scenes/global/Sidebar";
import Dashboard from "./scenes/dashboard";
import Team from "./scenes/team";
import StockScreener from "./scenes/stockScreener";
import Contacts from "./scenes/contacts";
import Bar from "./scenes/bar";
import Form from "./scenes/form";
import Line from "./scenes/line";
import Pie from "./scenes/pie";
import FAQ from "./scenes/faq";
import {CssBaseline, ThemeProvider} from "@mui/material";
import {ColorModeContext, useMode} from "./theme";
import StockProfile from "./scenes/stockProfile";
import Welcome from "./scenes/welcome";
import Register from "./scenes/register";
import Confirm from "./scenes/confirm";
import Login from "./scenes/login";
import AuthContext from './components/AuthContext';

function App() {
    const [theme, colorMode] = useMode();
    const [name, setName] = useState('');
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
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
                                <Route path="/" element={isAuthenticated ? (<Dashboard/>) : (
                                    <Navigate to="/welcome" replace/>)}/>
                                <Route path="/stockProfile/:stock_name" element={<StockProfile/>}/>
                                <Route path="/welcome" element={<Welcome/>}/>
                                <Route path="/register" element={<Register/>}/>
                                <Route path="/confirm" element={<Confirm/>}/>
                                <Route path="/login" element={<Login/>}/>
                                <Route path="/team" element={<Team/>}/>
                                <Route path="/contacts" element={<Contacts/>}/>
                                <Route path="/stockScreener" element={<StockScreener/>}/>
                                <Route path="/form" element={<Form/>}/>
                                <Route path="/bar" element={<Bar/>}/>
                                <Route path="/pie" element={<Pie/>}/>
                                <Route path="/line" element={<Line/>}/>
                                <Route path="/faq" element={<FAQ/>}/>
                            </Routes>
                        </main>
                    </div>
                </ThemeProvider>
            </ColorModeContext.Provider>
        </AuthContext.Provider>
    );
}

export default App;

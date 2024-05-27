from db_crudl import DatabaseCRUDL

dc = DatabaseCRUDL()

# Committees
dc.createCommittee('Budget and Finance Committee')
dc.createCommittee('Publication Committee')
dc.createCommittee('Logistics Committee')

# Constituents
dc.createConstituent('John Doe', 'john.doe@example.com', '2023-05-01', 1)
dc.createConstituent('Jane Smith', 'jane.smith@example.com', '2023-05-01', 1)
dc.createConstituent('Michael Johnson', 'michael.johnson@example.com', '2023-05-01', 2)
dc.createConstituent('Emily Davis', 'emily.davis@example.com', '2023-05-01', 2)
dc.createConstituent('David Wilson', 'david.wilson@example.com', '2023-05-01', 3)
dc.createConstituent('Sophia Miller', 'sophia.miller@example.com', '2023-05-01', 3)
dc.createConstituent('William Anderson', 'william.anderson@example.com', '2023-05-01', 1)
dc.createConstituent('Olivia Taylor', 'olivia.taylor@example.com', '2023-05-01', 1)
dc.createConstituent('James Thompson', 'james.thompson@example.com', '2023-05-01', 2)
dc.createConstituent('Emma Martinez', 'emma.martinez@example.com', '2023-05-01', 2)

# Events
dc.createEvent('Nantong Debate Cup 2023', '2023-06-01', '2023-06-03', 'Guizhong, China')
dc.createEvent('World Universities Debating Championship 2023', '2023-06-04', '2023-06-04', 'Universidad Rey Juan Carlos & Universidad Autónoma de Madrid')
dc.createEvent('Philippine Debate Union Cup 2023', '2023-06-05', '2023-06-05', 'Makati, Philippines')
dc.createEvent('Petron Debate Cup 2023', '2023-05-15', '2023-05-15', 'Tibanga, Iligan City')
dc.createEvent('STEM Debate Open', '2023-06-05', '2023-06-05', 'Philippine Science High School - Caraga Region Campus, Philippines')

# Awards
dc.createAward('Best Speaker', '2023-06-05', 5)
dc.createAward('Runner-up Best Speaker', '2023-06-05', 5)
dc.createAward('Best Debater', '2023-06-05', 5)
dc.createAward('Runner-up Best Debater', '2023-06-05', 5)
dc.createAward('Best Rebuttal', '2023-06-05', 5)
dc.createAward('Best Case Construction', '2023-06-05', 5)
dc.createAward('Most Improved Debater', '2023-06-05', 5)
dc.createAward('Spirit of Debate Award', '2023-06-05', 5)
dc.createAward('Judges Appreciation Award', '2023-06-05', 5)
dc.createAward('Organizing Committee Appreciation Award', '2023-06-05', 5)

# Constituent-Award Mappings
dc.createConstituentAward(1, 1)
dc.createConstituentAward(2, 2)
dc.createConstituentAward(3, 3)
dc.createConstituentAward(4, 4)
dc.createConstituentAward(5, 5)
dc.createConstituentAward(6, 6)
dc.createConstituentAward(7, 7)
dc.createConstituentAward(8, 8)
dc.createConstituentAward(9, 9)
dc.createConstituentAward(10, 10)

# Constituent-Event Mappings
dc.createConstituentEvent(1, 1)
dc.createConstituentEvent(1, 2)
dc.createConstituentEvent(1, 3)
dc.createConstituentEvent(2, 1)
dc.createConstituentEvent(2, 2)
dc.createConstituentEvent(2, 3)
dc.createConstituentEvent(3, 4)
dc.createConstituentEvent(4, 4)
dc.createConstituentEvent(5, 5)
dc.createConstituentEvent(6, 5)
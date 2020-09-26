"""
 *****************************************************************************
   FILE:splendor

   AUTHOR: BELAL SHAHEEN

   ASSIGNMENT:Final Project: Splendor

   DATE:11/13/2019

   DESCRIPTION:

 *****************************************************************************
"""
import os

alphabets = ['e','d','s','o','r']
prestige_points = ['1','2','3','4']

#card will return [pp,gem,'r','d','s','o','e']
def cardimporter_yuh(directory):
    dictionary = {}
    for filename in os.listdir(directory):

        if not filename.startswith("."):
            dictionary[filename] = [0,'',0,0,0,0,0]
            prestige = False
            gem = False
            name = filename.split('_')
            name[-1] = name[-1][:-4]
            for alphabet in alphabets:
                if alphabet in name[0]:
                    gem = True
                    break
                else:
                    gem = False

            for number in prestige_points:
                if number in name[0]:
                    prestige = True
                    break
                else:
                    prestige = False

            price = name[1:]

            if gem and prestige:
                value = name[0].split('.')
                dictionary[filename][0] = int(value[0])
                dictionary[filename][1] = value[1]
            elif gem:
                dictionary[filename][1] = name[0]
            else:
                dictionary[filename][0] = int(name[0])


            for thing in price:
                value = thing.split('.')
                amount = value[0]
                gem_needed = value[1]
                if gem_needed == 'r':
                    dictionary[filename][2] = amount
                if gem_needed == 'd':
                    dictionary[filename][3] = amount
                if gem_needed == 's':
                    dictionary[filename][4] = amount
                if gem_needed == 'o':
                    dictionary[filename][5] = amount
                if gem_needed == 'e':
                    dictionary[filename][6] = amount

    return dictionary
